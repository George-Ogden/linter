from collections.abc import Sequence
from typing import ClassVar

import libcst as cst
import libcst.matchers as m

from ..rule import Rule


class FrozendictDictRule(Rule[cst.Call]):
    node_names: ClassVar[tuple[str]] = ("Call",)
    rule_name: ClassVar[str] = "frozendict-dict"

    @classmethod
    def check(cls, node: cst.Call) -> bool:
        return not m.matches(
            node,
            m.Call(
                m.Name("frozendict") | m.Attribute(m.Name("frozendict"), m.Name("frozendict")),
                [
                    m.Arg(m.Call(m.Name("dict")), keyword=None, star="")
                    | m.Arg(star="**")
                    | m.Arg(m.Dict([]), star="", keyword=None)
                ],
            ),
        )

    @classmethod
    def fix(cls, node: cst.Call) -> cst.BaseExpression | None:
        callee = node.func
        [arg] = node.args
        args: Sequence[cst.Arg]
        if arg.star == "**":
            args = [arg.with_changes(star="")]
            whitespace_before_args = node.whitespace_before_args
        elif isinstance(arg.value, cst.Dict):
            args = []
            whitespace_before_args = cst.SimpleWhitespace("")
        else:
            assert isinstance(arg.value, cst.Call)
            args = arg.value.args
            whitespace_before_args = arg.value.whitespace_before_args

        return cst.Call(
            callee,
            args,
            lpar=node.lpar,
            rpar=node.rpar,
            whitespace_after_func=node.whitespace_after_func,
            whitespace_before_args=whitespace_before_args,
        )
