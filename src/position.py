from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    line: int  # one-based indexing
    char: int  # one-based indexing


@dataclass(frozen=True)
class Location:
    filename: str
    position: Position | None
