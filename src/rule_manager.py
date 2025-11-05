from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import KW_ONLY, dataclass
import functools
from typing import Any, Self

import libcst as cst

from .rule import Rule


@dataclass
class RuleManager(cst.CSTTransformer):
    rules: Sequence[type[Rule]]
    _: KW_ONLY
    fix: bool

    def check_rule[NodeT: cst.BaseExpression](
        self, original_node: NodeT, updated_node: NodeT, *, rules: Sequence[type[Rule[NodeT, Any]]]
    ) -> cst.BaseExpression:
        for rule in rules:
            rule.check(original_node, updated_node)
        return updated_node

    def __post_init__(self) -> None:
        rule_groups = self._group_rules_by_node_names(self.rules)
        for node_name, rules in rule_groups.items():
            setattr(self, f"leave_{node_name}", functools.partial(self.check_rule, rules=rules))

    @classmethod
    def _group_rules_by_node_names(
        cls, rules: Sequence[type[Rule]]
    ) -> Mapping[str, Sequence[type[Rule]]]:
        rule_groups = defaultdict(list)
        for rule in rules:
            for node_name in rule.node_names:
                rule_groups[node_name].append(rule)
        return rule_groups

    @classmethod
    def from_rule_names(cls, *rule_names: str, fix: bool) -> Self:
        return cls([Rule.rules[rule_name] for rule_name in rule_names], fix=fix)
