from collections.abc import Sequence
from dataclasses import dataclass
import itertools

from .report import Report
from .rule_manager import RuleManager


@dataclass(kw_only=True)
class LinterConfig:
    included_rule_names: list[str]
    fix: bool
    filenames: Sequence[str]

    def run(self) -> Report:
        file_checker = RuleManager.from_rule_names(*self.included_rule_names, fix=self.fix)
        report = Report.from_feedback(
            itertools.chain.from_iterable(
                file_checker.lint_file(filename) for filename in self.filenames
            )
        )
        report.display()
        return report
