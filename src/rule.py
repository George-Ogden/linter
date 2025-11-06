from __future__ import annotations

import abc
from collections.abc import Mapping
from typing import Any, ClassVar, Final

import libcst as cst


class Rule[NodeT: cst.BaseExpression, CheckT](abc.ABC):
    rules: Final[Mapping[str, type[Rule]]] = {}
    rule_name: ClassVar[str]
    node_names: ClassVar[tuple[str, ...]]

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls()
        cls.node_names  # noqa: B018
        assert cls.rule_name not in cls.rules
        cls.rules[cls.rule_name] = cls  # type: ignore[index]

    @classmethod
    @abc.abstractmethod
    def check(cls, node: NodeT) -> CheckT | None: ...

    @classmethod
    @abc.abstractmethod
    def fix(cls, info: CheckT, /) -> cst.BaseExpression | None: ...
