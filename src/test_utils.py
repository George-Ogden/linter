from collections.abc import Iterable
import os.path
from typing import ClassVar
from unittest import mock

import libcst as cst

from .position import Position
from .rule import Rule
from .rule_manager import RuleManager


class RuleMock[NodeT: cst.BaseExpression](Rule[NodeT, None]):
    _mock: ClassVar[mock.MagicMock] = mock.MagicMock()
    rule_name = "rule-mock"
    node_names: ClassVar[tuple[str, ...]] = ()

    @classmethod
    def check(cls, node: NodeT) -> None:
        raise NotImplementedError()

    @classmethod
    def fix(cls, info: None) -> None: ...


def check_rules_test_body(
    rules: Iterable[str], filename: str, expected_positions: list[tuple[int, int]]
) -> None:
    file_checker = RuleManager.from_rule_names(*rules, fix=False)
    filename = os.path.join("test_data/", filename)
    violation_positions = [location.position for location, _ in file_checker.lint_file(filename)]
    expected = [Position(line, char) for line, char in expected_positions]
    assert violation_positions == expected
