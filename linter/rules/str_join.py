import dataclasses
from typing import ClassVar

import libcst as cst
import libcst.matchers as m

from ..rule import Rule


class StrJoinRule(Rule[cst.Call]):
    node_names: ClassVar[tuple[str]] = ("Call",)
    rule_name: ClassVar[str] = "str-join"

    @classmethod
    def check(cls, node: cst.Call) -> bool:
        return not m.matches(
            node,
            m.Call(
                m.Attribute(
                    m.SimpleString() | m.FormattedString() | m.ConcatenatedString(), m.Name("join")
                ),
                [m.Arg(keyword=None, star="")],
            ),
        )

    @classmethod
    def fix(cls, node: cst.Call) -> cst.BaseExpression:
        assert isinstance(node.func, cst.Attribute)
        [arg] = node.args
        if isinstance(arg.value, cst.GeneratorExp) and not (arg.value.lpar and arg.value.rpar):
            arg = dataclasses.replace(
                arg,
                value=dataclasses.replace(
                    arg.value, lpar=[cst.LeftParen()], rpar=[cst.RightParen()]
                ),
            )
        return cst.Call(
            cst.Attribute(cst.Name("str"), cst.Name("join")),
            [cst.Arg(node.func.value), arg],
            lpar=node.lpar,
            rpar=node.rpar,
            whitespace_after_func=node.whitespace_after_func,
            whitespace_before_args=node.whitespace_before_args,
        )
