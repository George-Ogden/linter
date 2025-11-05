from typing import ClassVar
from unittest import mock

import libcst as cst

from .rule import Rule


class RuleMock[NodeT: cst.BaseExpression](Rule[NodeT, None]):
    _mock: ClassVar[mock.MagicMock] = mock.MagicMock()
    rule_name = "rule-mock"

    @classmethod
    def fix(cls, info: None) -> None: ...

    @classmethod
    def check(cls, original_node: NodeT, updated_node: NodeT) -> None:
        raise NotImplementedError()
