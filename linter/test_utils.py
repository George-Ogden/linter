from __future__ import annotations

from collections.abc import Sequence
import difflib
import filecmp
import os
from pathlib import Path
import shutil
import tempfile
from typing import TYPE_CHECKING, ClassVar, Final, cast
from unittest import mock

from .feedback import Violation
from .position import Position
from .rule import NodeT, Rule
from .rule_manager import RuleManager

TEST_DATA_DIR: Final[Path] = Path("test_data/")

if TYPE_CHECKING:
    from mypy_pytest_plugin_types.mock import MagicMock


class RuleMock(Rule[NodeT]):
    _mock: ClassVar[MagicMock] = mock.MagicMock()
    rule_name = "rule-mock"
    node_names: ClassVar[tuple[str, ...]] = ()

    @classmethod
    def check(cls, node: NodeT) -> bool:
        raise NotImplementedError()

    @classmethod
    def fix(cls, info: NodeT) -> None: ...


def check_rules_test_body(
    rules: Sequence[str], filename: str, expected_positions: list[tuple[int, int]]
) -> None:
    file_checker = RuleManager.from_rule_names(*rules, fix=False)
    violations = list(file_checker.lint_file(str(TEST_DATA_DIR / filename)))
    assert all(isinstance(violation, Violation) for violation in violations)
    violation_positions = [cast(Position, violation.location.position) for violation in violations]
    expected = [Position(line, char) for line, char in expected_positions]
    violation_positions.sort()
    expected.sort()
    assert violation_positions == expected
    assert all(not cast(Violation, violation).fixed for violation in violations)


def fix_rules_test_body(rules: Sequence[str], filename: str, expected_filename: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_filepath = Path(temp_dir) / os.path.basename(filename)
        shutil.copy2(TEST_DATA_DIR / filename, temp_filepath)
        rule_manager = RuleManager.from_rule_names(*rules, fix=True)
        violations = list(rule_manager.lint_file(str(temp_filepath)))
        assert all(isinstance(violation, Violation) for violation in violations)
        assert all(cast(Violation, violation).fixed for violation in violations)

        with open(temp_filepath) as f:
            source = f.read()
            print(source)

        expected_path = TEST_DATA_DIR / expected_filename
        with open(expected_path) as f:
            expected = f.read()

        assert filecmp.cmp(temp_filepath, expected_path), "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                source.splitlines(),
                fromfile=str(expected_path),
                tofile=filename,
            )
        )
