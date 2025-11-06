from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    line: int  # one-based indexing
    char: int  # one-based indexing

    def format(self) -> str:
        return f"{self.line}:{self.char}"


@dataclass(frozen=True)
class Location:
    filename: str
    position: Position | None

    def format(self) -> str:
        return f"{self.filename}{'' if self.position is None else f':{self.position.format()}'}"
