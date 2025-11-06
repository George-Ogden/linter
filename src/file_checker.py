from collections.abc import Iterable, Sequence
from dataclasses import dataclass
import functools
from typing import Any, ClassVar

import libcst as cst
from libcst._position import CodeRange
import libcst.metadata as metadata

from .noqa_finder import IgnoredLines, NoqaFinder
from .position import Location, Position
from .rule import Rule
from .violation import Violation


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
        try:  # noqa: SIM105
            self.module = cst.parse_module("".join(self.lines))
        except (SyntaxError, ValueError):
            ...

    def wrap_metadata(self) -> None:
        self.wrapper = cst.MetadataWrapper(self.module)

    def check_rules[NodeT: cst.BaseExpression](
        self, original_node: NodeT, updated_node: NodeT, *, rules: Sequence[type[Rule[NodeT, Any]]]
    ) -> cst.BaseExpression:
        for rule in rules:
            if self.applies_to_line(rule, self.get_line(original_node)):
                result = rule.check(original_node)
                if result is not None:
                    self.violations.append(self.violation_from_node(original_node))
        return updated_node

    @functools.cached_property
    def ignored_codes(self) -> IgnoredLines:
        return NoqaFinder.parse_lines(self.lines)

    def applies_to_line(self, rule: type[Rule], line: int | None) -> bool:
        return line is None or rule.rule_name not in self.ignored_codes.get(line, ())

    def violation_from_node(self, node: cst.BaseExpression) -> Violation:
        position = self.get_position(node)
        return Violation(Location(self.filename, position), node)

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
        self.wrapper.visit(self)

    @classmethod
    def lint_file(cls, filename: str) -> Iterable[Violation]:
        linter = cls(filename)
        linter.check()
        yield from linter.violations
