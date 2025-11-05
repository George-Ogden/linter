from __future__ import annotations

import abc
from typing import Any, ClassVar, Final

import libcst as cst


class Rule[NodeT: cst.BaseExpression, CheckT](abc.ABC):
    rules: Final[dict[str, Any]] = {}
    rule_name: ClassVar[str]
    node_names: ClassVar[tuple[str, ...]]

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls()
        assert cls.rule_name not in cls.rules
        cls.rules[cls.rule_name] = cls

    @classmethod
    @abc.abstractmethod
    def check(cls, original_node: NodeT, updated_node: NodeT) -> CheckT | None: ...

    @classmethod
    @abc.abstractmethod
    def fix(cls, info: CheckT) -> cst.BaseExpression | None: ...
