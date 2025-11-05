from typing import ClassVar
from unittest import mock

import libcst as cst

from .rule_manager import RuleManager
from .test_utils import RuleMock


class IntegerRuleMock(RuleMock[cst.Integer]):
    rule_name: ClassVar[str] = "integer-mock"
    node_names: ClassVar[tuple[str]] = ("Integer",)

    @classmethod
    def check(cls, original_node: cst.Integer, updated_node: cst.Integer) -> None:
        cls._mock(original_node.evaluated_value, updated_node.evaluated_value)


class StringRuleMock(RuleMock[cst.SimpleString]):
    rule_name: ClassVar[str] = "string-mock"
    node_names: ClassVar[tuple[str]] = ("SimpleString",)
    _mock: ClassVar[mock.MagicMock] = mock.MagicMock()

    @classmethod
    def check(cls, original_node: cst.SimpleString, updated_node: cst.SimpleString) -> None:
        cls._mock(original_node.evaluated_value, updated_node.evaluated_value)


class StringAndIntegerRuleMock(RuleMock[cst.Integer | cst.SimpleString]):
    rule_name: ClassVar[str] = "string-integer-mock"
    node_names: ClassVar[tuple[str, str]] = ("SimpleString", "Integer")
    _mock: ClassVar[mock.MagicMock] = mock.MagicMock()

    @classmethod
    def check(
        cls,
        original_node: cst.Integer | cst.SimpleString,
        updated_node: cst.Integer | cst.SimpleString,
    ) -> None:
        cls._mock(original_node.evaluated_value, updated_node.evaluated_value)

    @classmethod
    def fix(cls, info: None) -> None: ...


def test_integer_rule_registers_correctly_and_runs_on_integers() -> None:
    rule_manager = RuleManager([IntegerRuleMock], fix=False)
    with mock.patch.object(IntegerRuleMock, "_mock") as m:
        cst.Integer("10").visit(rule_manager)
    m.assert_called_once_with(10, 10)


def test_integer_rule_registers_correctly_and_does_not_run_on_strings() -> None:
    rule_manager = RuleManager([IntegerRuleMock], fix=False)
    with mock.patch.object(IntegerRuleMock, "_mock") as m:
        cst.SimpleString("'10'").visit(rule_manager)
    m.assert_not_called()


def test_integer_rule_registers_correctly_and_runs_twice() -> None:
    rule_manager = RuleManager([IntegerRuleMock], fix=False)
    with mock.patch.object(IntegerRuleMock, "_mock") as m:
        cst.List([cst.Element(cst.Integer("10")), cst.Element(cst.Integer("5"))]).visit(
            rule_manager
        )
    m.assert_has_calls([mock.call(10, 10), mock.call(5, 5)])


def test_integer_rule_registers_multiple_correctly_and_runs_both() -> None:
    rule_manager = RuleManager([IntegerRuleMock, StringRuleMock], fix=False)
    with (
        mock.patch.object(IntegerRuleMock, "_mock") as im,
        mock.patch.object(StringRuleMock, "_mock") as sm,
    ):
        cst.List([cst.Element(cst.Integer("4")), cst.Element(cst.SimpleString("'4'"))]).visit(
            rule_manager
        )
    im.assert_has_calls([mock.call(4, 4)])
    sm.assert_has_calls([mock.call("4", "4")])


def test_integer_rule_registers_multiple_correctly_and_runs_all_rules() -> None:
    rule_manager = RuleManager(
        [IntegerRuleMock, StringRuleMock, StringAndIntegerRuleMock], fix=False
    )
    with (
        mock.patch.object(IntegerRuleMock, "_mock") as im,
        mock.patch.object(StringRuleMock, "_mock") as sm,
        mock.patch.object(StringAndIntegerRuleMock, "_mock") as sim,
    ):
        cst.List([cst.Element(cst.Integer("4")), cst.Element(cst.SimpleString("'4'"))]).visit(
            rule_manager
        )
    im.assert_has_calls([mock.call(4, 4)])
    sm.assert_has_calls([mock.call("4", "4")])
    sim.assert_has_calls([mock.call(4, 4), mock.call("4", "4")])


def test_rule_registration_one_rule() -> None:
    rule_manager = RuleManager.from_rule_names("integer-mock", fix=False)
    assert rule_manager.rules == [IntegerRuleMock]


def test_rule_registration_many_rules() -> None:
    rule_manager = RuleManager.from_rule_names(
        "integer-mock", "string-mock", "string-integer-mock", fix=False
    )
    assert rule_manager.rules == [IntegerRuleMock, StringRuleMock, StringAndIntegerRuleMock]
