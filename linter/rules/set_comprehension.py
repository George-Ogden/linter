from typing import ClassVar, cast

import libcst as cst
import libcst.matchers as m

from ..rule import Rule


class SetComprehensionRule(Rule[cst.Call]):
    node_names: ClassVar[tuple[str]] = ("Call",)
    rule_name: ClassVar[str] = "set-comprehension"

    @classmethod
    def check(cls, node: cst.Call) -> bool:
        return not m.matches(
            node,
            m.Call(
                m.Name("set"),
                [
                    m.Arg(
                        m.GeneratorExp() | m.SetComp(),
                        keyword=None,
                        star="",
                    )
                ],
            ),
        )

    @classmethod
    def fix(cls, node: cst.Call) -> cst.BaseExpression | None:
        [arg] = node.args
        comp = cast(cst.GeneratorExp | cst.SetComp, arg.value)
        match comp:
            case cst.GeneratorExp():
                lbrace = cst.LeftCurlyBrace(whitespace_after=node.whitespace_before_args)
                rbrace = cst.RightCurlyBrace(arg.whitespace_after_arg)
            case cst.SetComp():
                lbrace = comp.lbrace
                rbrace = comp.rbrace
            case _:
                raise TypeError()
        return cst.SetComp(elt=comp.elt, for_in=comp.for_in, lbrace=lbrace, rbrace=rbrace)
