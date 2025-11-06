from dataclasses import dataclass
import textwrap

from .position import Location


@dataclass
class Error:
    location: Location
    message: str

    def format(self) -> str:
        return f"{self.location.format()}: {self.message}"


@dataclass
class Violation:
    location: Location
    code: str
    fixed: bool

    def fix(self) -> None:
        self.fixed = True

    def format(self) -> str:
        return f"{self.location.format()}: {self.format_code(self.code)}"

    @classmethod
    def format_code(cls, code: str) -> str:
        first_line, *lines = code.split("\n", maxsplit=1)
        if lines:
            [line] = lines
            return f"{first_line}\n{textwrap.dedent(line)}"
        return first_line
