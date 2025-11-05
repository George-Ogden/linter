from __future__ import annotations

import abc
from typing import Any, ClassVar, Final

import libcst as cst


class Rule[NodeT: cst.BaseExpression, CheckT](abc.ABC):
    rules: Final[dict[str, Any]] = {}
    rulename: ClassVar[str]
    node_names: ClassVar[tuple[str, ...]]

    @classmethod
    @abc.abstractmethod
    def check(cls, original_node: NodeT, updated_node: NodeT) -> CheckT | None: ...

    @classmethod
    @abc.abstractmethod
    def fix(cls, info: CheckT) -> cst.BaseExpression | None: ...
