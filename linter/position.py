from dataclasses import dataclass

from typing_extensions import Self


@dataclass(frozen=True)
class Position:
    line: int  # one-based indexing
    char: int  # one-based indexing

    def format(self) -> str:
        return f"{self.line}:{self.char}"

    def __lt__(self, other: Self) -> bool:
        return (self.line, self.char) < (other.line, other.char)


@dataclass(frozen=True)
class Location:
    filename: str
    position: Position | None

    def format(self) -> str:
        return f"{self.filename}{'' if self.position is None else f':{self.position.format()}'}"
