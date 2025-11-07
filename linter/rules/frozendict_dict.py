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
        raise NotImplementedError()
