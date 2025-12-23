from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar
from unittest import mock

import libcst as cst
import pytest

from .file_checker import FileChecker
from .rule_manager import RuleManager
from .test_utils import RuleMock

if TYPE_CHECKING:
    from mypy_pytest_plugin_types.mock import MagicMock


class IntegerRuleMock(RuleMock[cst.Integer]):
    rule_name: ClassVar[str] = "integer-mock"
    node_names: ClassVar[tuple[str]] = ("Integer",)

    @classmethod
    def check(cls, node: cst.Integer) -> bool:
        cls._mock(node.evaluated_value)
        return True


class StringRuleMock(RuleMock[cst.SimpleString]):
    rule_name: ClassVar[str] = "string-mock"
    node_names: ClassVar[tuple[str]] = ("SimpleString",)
    _mock: ClassVar[MagicMock] = mock.MagicMock()

    @classmethod
    def check(cls, node: cst.SimpleString) -> bool:
        cls._mock(node.evaluated_value)
        return True


class StringAndIntegerRuleMock(RuleMock[cst.Integer | cst.SimpleString]):
    rule_name: ClassVar[str] = "string-integer-mock"
    node_names: ClassVar[tuple[str, str]] = ("SimpleString", "Integer")
    _mock: ClassVar[MagicMock] = mock.MagicMock()

    @classmethod
    def check(cls, node: cst.Integer | cst.SimpleString) -> bool:
        cls._mock(node.evaluated_value)
        return True


@pytest.fixture
def mock_file() -> Any:
    with (
        mock.patch.object(FileChecker, "__post_init__") as m,
        mock.patch.object(FileChecker, "get_metadata", return_value=None),
    ):
        yield m


def test_integer_rule_registers_correctly_and_runs_on_integers(
    mock_file: pytest.FixtureDef,
) -> None:
    linter = RuleManager.from_rules([IntegerRuleMock], fix=False)("")
    with mock.patch.object(IntegerRuleMock, "_mock") as m:
        cst.Integer("10").visit(linter)
    m.assert_called_once_with(10)


def test_integer_rule_registers_correctly_and_does_not_run_on_strings(
    mock_file: pytest.FixtureDef,
) -> None:
    linter = RuleManager.from_rules([IntegerRuleMock], fix=False)("")
    with mock.patch.object(IntegerRuleMock, "_mock") as m:
        cst.SimpleString("'10'").visit(linter)
    m.assert_not_called()


def test_integer_rule_registers_correctly_and_runs_twice(mock_file: pytest.FixtureDef) -> None:
    linter = RuleManager.from_rules([IntegerRuleMock], fix=False)("")
    with mock.patch.object(IntegerRuleMock, "_mock") as m:
        cst.List([cst.Element(cst.Integer("10")), cst.Element(cst.Integer("5"))]).visit(linter)
    m.assert_has_calls([mock.call(10), mock.call(5)])


def test_integer_rule_registers_multiple_correctly_and_runs_both(
    mock_file: pytest.FixtureDef,
) -> None:
    linter = RuleManager.from_rules([IntegerRuleMock, StringRuleMock], fix=False)("")
    with (
        mock.patch.object(IntegerRuleMock, "_mock") as im,
        mock.patch.object(StringRuleMock, "_mock") as sm,
    ):
        cst.List([cst.Element(cst.Integer("4")), cst.Element(cst.SimpleString("'4'"))]).visit(
            linter
        )
    im.assert_has_calls([mock.call(4)])
    sm.assert_has_calls([mock.call("4")])


def test_integer_rule_registers_multiple_correctly_and_runs_all_rules(
    mock_file: pytest.FixtureDef,
) -> None:
    linter = RuleManager.from_rules(
        [IntegerRuleMock, StringRuleMock, StringAndIntegerRuleMock], fix=False
    )("")
    with (
        mock.patch.object(IntegerRuleMock, "_mock") as im,
        mock.patch.object(StringRuleMock, "_mock") as sm,
        mock.patch.object(StringAndIntegerRuleMock, "_mock") as sim,
    ):
        cst.List([cst.Element(cst.Integer("4")), cst.Element(cst.SimpleString("'4'"))]).visit(
            linter
        )
    im.assert_has_calls([mock.call(4)])
    sm.assert_has_calls([mock.call("4")])
    sim.assert_has_calls([mock.call(4), mock.call("4")])


def test_rule_registration_one_rule() -> None:
    linter = RuleManager.from_rule_names("integer-mock", fix=False)
    assert linter.rules == [IntegerRuleMock]


def test_rule_registration_many_rules() -> None:
    linter = RuleManager.from_rule_names(
        "integer-mock", "string-mock", "string-integer-mock", fix=False
    )
    assert linter.rules == [IntegerRuleMock, StringRuleMock, StringAndIntegerRuleMock]
