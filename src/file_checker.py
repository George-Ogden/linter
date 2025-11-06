from collections.abc import Iterable, Sequence
from dataclasses import dataclass
import functools
from typing import ClassVar

import libcst as cst
from libcst._position import CodeRange
import libcst.metadata as metadata

from .feedback import Error, Violation
from .noqa_finder import IgnoredLines, NoqaFinder
from .position import Location, Position
from .rule import Rule


@dataclass
class FileChecker(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (metadata.PositionProvider,)
    fix: ClassVar[bool]
    rules: ClassVar[Sequence[type[Rule]]]
    filename: str

    def __post_init__(self) -> None:
        self.read_file()
        self.parse_file()
        self.wrap_metadata()
        self.violations: list[Violation] = []

    def read_file(self) -> None:
        with open(self.filename) as f:
            self.lines = f.readlines()

    def parse_file(self) -> None:
        self.module = cst.parse_module("".join(self.lines))

    def wrap_metadata(self) -> None:
        self.wrapper = cst.MetadataWrapper(self.module)

    def check_rules[NodeT: cst.BaseExpression](
        self, original_node: NodeT, updated_node: NodeT, *, rules: Sequence[type[Rule[NodeT]]]
    ) -> cst.BaseExpression:
        for rule in rules:
            if self.applies_to_line(rule, self.get_line(original_node)):
                check_result = rule.check(original_node)
                if not check_result:
                    violation = self.report_violation(original_node)
                    if self.fix:
                        fix_result = rule.fix(updated_node)
                        if fix_result is not None:
                            violation.fix()
                            return fix_result
        return updated_node

    def report_violation(self, node: cst.BaseExpression) -> Violation:
        violation = self.violation_from_node(node)
        self.violations.append(violation)
        return violation

    @functools.cached_property
    def ignored_codes(self) -> IgnoredLines:
        return NoqaFinder.parse_lines(self.lines)

    def applies_to_line(self, rule: type[Rule], line: int | None) -> bool:
        return line is None or rule.rule_name not in self.ignored_codes.get(line, ())

    def violation_from_node(self, node: cst.BaseExpression) -> Violation:
        position = self.get_position(node)
        return Violation(Location(self.filename, position), node, fixed=False)

    def get_position(self, node: cst.BaseExpression) -> None | Position:
        range: CodeRange | None = self.get_metadata(metadata.PositionProvider, node)
        position = None if range is None else Position(range.start.line, range.start.column + 1)
        return position

    def get_line(self, node: cst.BaseExpression) -> None | int:
        position = self.get_position(node)
        if position is None:
            return None
        return position.line

    def check(self) -> None:
        updated_node = self.wrapper.visit(self)
        if self.made_changes:
            self.overwrite(updated_node)

    @property
    def made_changes(self) -> bool:
        return any(violation.fixed for violation in self.violations)

    def overwrite(self, node: cst.Module) -> None:
        with open(self.filename, "w") as f:
            f.write(node.code)

    @classmethod
    def lint_file(cls, filename: str) -> Iterable[Error | Violation]:
        try:
            linter = cls(filename)
        except cst.ParserSyntaxError as e:
            yield Error(Location(filename, Position(e.raw_line, e.raw_column + 1)), "Syntax Error")
            return
        except OSError as e:
            yield Error(Location(filename, None), type(e).__name__)
            return
        linter.check()
        yield from linter.violations
