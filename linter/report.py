from collections.abc import Iterable, Sequence
from dataclasses import dataclass
import functools

from typing_extensions import Self

from .feedback import Error, Violation


@dataclass
class Report:
    errors: Sequence[Error]
    violations: Sequence[Violation]

    def display(self) -> None:
        for error in self.errors:
            print(error.format())
        for violation in self.violations:
            if not violation.fixed:
                print(violation.format())
        if self.num_fixes:
            print(self.format_fixes())

    def format_fixes(self) -> str:
        num_fixes = self.num_fixes
        fix_suffix = "" if num_fixes == 1 else "es"
        return f"{num_fixes} fix{fix_suffix} applied"

    @functools.cached_property
    def num_fixes(self) -> int:
        return sum(violation.fixed for violation in self.violations)

    @classmethod
    def from_feedback(cls, feedback: Iterable[Error | Violation]) -> Self:
        errors = []
        violations = []
        for feedback_item in feedback:
            match feedback_item:
                case Error() as error:
                    errors.append(error)
                case Violation() as violation:
                    violations.append(violation)
                case _:
                    raise TypeError()
        return cls(errors, violations)

    def __bool__(self) -> bool:
        return bool(self.errors or self.violations)
