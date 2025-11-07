from __future__ import annotations

import abc
from collections.abc import Mapping
from typing import Any, ClassVar, Final, Generic, TypeVar

import libcst as cst

NodeT = TypeVar("NodeT", bound=cst.BaseExpression)


class Rule(abc.ABC, Generic[NodeT]):
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
    def check(cls, node: NodeT) -> bool: ...

    @classmethod
    @abc.abstractmethod
    def fix(cls, node: NodeT, /) -> cst.BaseExpression | None: ...
