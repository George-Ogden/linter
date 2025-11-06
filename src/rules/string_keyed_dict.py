import keyword
from typing import ClassVar, cast

import libcst as cst
import libcst.matchers as m

from ..rule import Rule


class StringKeyedDictRule(Rule[cst.Dict]):
    node_names: ClassVar[tuple[str]] = ("Dict",)
    rule_name: ClassVar[str] = "string-keyed-dict"

    @classmethod
    def check(cls, node: cst.Dict) -> bool:
        existing_elements: list[cst.DictElement] = [
            cast(cst.DictElement, element)
            for element in node.elements
            if m.matches(element, m.DictElement())
        ]
        return not bool(
            existing_elements
            and all(cls._is_compatible_element(element) for element in existing_elements)
        )

    @classmethod
    def _is_compatible_element(cls, element: cst.DictElement) -> bool:
        return (
            m.matches(element.key, m.SimpleString())
            and cast(cst.SimpleString, element.key).raw_value.isidentifier()
            and not keyword.iskeyword(cast(cst.SimpleString, element.key).raw_value)
        )

    @classmethod
    def fix(cls, node: cst.Dict) -> cst.BaseExpression:
        args = [cls.element_to_arg(element) for element in node.elements]
        if args:
            args[-1] = cls.reformat_last_arg(args[-1], node.rbrace.whitespace_before)
        return cst.Call(
            cst.Name("dict"),
            whitespace_before_args=node.lbrace.whitespace_after,
            args=args,
        )

    @classmethod
    def reformat_last_arg(
        cls, arg: cst.Arg, whitespace: cst.BaseParenthesizableWhitespace
    ) -> cst.Arg:
        if isinstance(arg.comma, cst.MaybeSentinel):
            return arg
        return arg.with_changes(comma=arg.comma.with_changes(whitespace_after=whitespace))

    @classmethod
    def element_to_arg(cls, element: cst.BaseDictElement) -> cst.Arg:
        if isinstance(element, cst.DictElement):
            return cst.Arg(
                keyword=cst.Name(cast(cst.SimpleString, element.key).raw_value),
                value=element.value,
                equal=cst.AssignEqual(
                    whitespace_before=cst.SimpleWhitespace(""),
                    whitespace_after=cst.SimpleWhitespace(""),
                ),
                comma=element.comma,
            )
        return cst.Arg(
            value=element.value,
            star="**",
            comma=element.comma,
            whitespace_after_star=cast(cst.StarredDictElement, element).whitespace_before_value,
        )
