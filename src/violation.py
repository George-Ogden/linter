from typing import NamedTuple

import libcst as cst

from .position import Location


class Violation(NamedTuple):
    location: Location
    node: cst.BaseExpression
