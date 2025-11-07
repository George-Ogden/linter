from typing import ClassVar

import libcst as cst
import libcst.matchers as m

from ..rule import Rule


class SetComprehensionRule(Rule[cst.Call]):
    node_names: ClassVar[tuple[str]] = ("Call",)
    rule_name: ClassVar[str] = "set-comprehension"

    @classmethod
    def check(cls, node: cst.Call) -> bool:
        return not m.matches(
            node, m.Call(func=m.Name("set"), args=[m.Arg(m.GeneratorExp() | m.SetComp())])
        )

    @classmethod
    def fix(cls, node: cst.Call) -> cst.BaseExpression | None:
        raise NotImplementedError
