from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import KW_ONLY, dataclass
from typing import Any

import libcst as cst

from .file_checker import FileChecker
from .rule import Rule


@dataclass
class RuleManager(cst.CSTTransformer):
    rules: Sequence[type[Rule]]
    _: KW_ONLY
    fix: bool

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
    def from_rule_names(cls, *rule_names: str, fix: bool) -> type[FileChecker]:
        rules = [Rule.rules[rule_name] for rule_name in rule_names]
        return cls.from_rules(rules, fix=fix)

    @classmethod
    def from_rules(cls, rules: Sequence[type[Rule]], *, fix: bool) -> type[FileChecker]:
        return type(
            f"{FileChecker.__name__}[{','.join(rule.rule_name for rule in rules)}]",
            (FileChecker,),
            dict(rules=rules, fix=fix, **cls._rule_methods(rules)),
        )

    @classmethod
    def _rule_methods(cls, rules: Sequence[type[Rule]]) -> dict[str, Callable]:
        rule_groups = cls._group_rules_by_node_names(rules)

        return {
            f"leave_{node_name}": cls._rule_closure(rules)
            for node_name, rules in rule_groups.items()
        }

    @classmethod
    def _rule_closure(cls, rules: Sequence[type[Rule]]) -> Callable:
        def check_rules(self: FileChecker, *args: Any) -> Any:
            return self.check_rules(*args, rules=rules)

        return check_rules
