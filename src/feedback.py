from dataclasses import dataclass, field

import libcst as cst

from .position import Location


@dataclass
class Error:
    location: Location
    message: str


@dataclass
class Violation:
    location: Location
    node: cst.BaseExpression = field(repr=False)
    fixed: bool

    def fix(self) -> None:
        self.fixed = True
