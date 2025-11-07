from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

from typing_extensions import Self

T = TypeVar("T")


@dataclass(init=False, frozen=True)
class fullset(Generic[T]):  # noqa: N801
    _values: set[T] | None

    def __init__(self, items: Iterable[T] | None = ()) -> None:
        if items is not None:
            items = set(items)
        object.__setattr__(self, "_values", items)

    def union(self, other: Self) -> Self:
        if self._values is None or other._values is None:
            return type(self)(None)
        return type(self)(self._values.union(other._values))

    def add(self, item: T) -> None:
        if self._values is not None:
            self._values.add(item)

    def __bool__(self) -> bool:
        return self._values is None or bool(self._values)

    def __contains__(self, item: T, /) -> bool:
        return self._values is None or item in self._values
