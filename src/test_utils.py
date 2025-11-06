from collections.abc import Iterable
import filecmp
import os
from pathlib import Path
import shutil
import tempfile
from typing import ClassVar, Final
from unittest import mock

import libcst as cst

from .position import Position
from .rule import Rule
from .rule_manager import RuleManager

TEST_DATA_DIR: Final[Path] = Path("test_data/")


class RuleMock[NodeT: cst.BaseExpression](Rule[NodeT]):
    _mock: ClassVar[mock.MagicMock] = mock.MagicMock()
    rule_name = "rule-mock"
    node_names: ClassVar[tuple[str, ...]] = ()

    @classmethod
    def check(cls, node: NodeT) -> bool:
        raise NotImplementedError()

    @classmethod
    def fix(cls, info: NodeT) -> None: ...


def check_rules_test_body(
    rules: Iterable[str], filename: str, expected_positions: list[tuple[int, int]]
) -> None:
    file_checker = RuleManager.from_rule_names(*rules, fix=False)
    violations = file_checker.lint_file(str(TEST_DATA_DIR / filename))
    violation_positions = [violation.location.position for violation in violations]
    expected = [Position(line, char) for line, char in expected_positions]
    assert violation_positions == expected
    assert all(not violation.fixed for violation in violations)


def fix_rules_test_body(rules: Iterable[str], filename: str, expected_filename: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_filepath = Path(temp_dir) / os.path.basename(filename)
        shutil.copy2(TEST_DATA_DIR / filename, temp_filepath)
        rule_manager = RuleManager.from_rule_names(*rules, fix=True)
        violations = list(rule_manager.lint_file(str(temp_filepath)))
        assert all(violation.fixed for violation in violations)

        with open(temp_filepath) as f:
            source = f.read()
            print(source)

        assert filecmp.cmp(temp_filepath, TEST_DATA_DIR / expected_filename)
