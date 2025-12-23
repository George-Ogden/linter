import pytest

from .feedback import Error
from .position import Location, Position
from .rule import Rule
from .rule_manager import RuleManager
from .test_utils import TEST_DATA_DIR, fix_rules_test_body


def test_check_syntax_error_returns_error() -> None:
    linter = RuleManager.from_rule_names(fix=False)
    filename = str(TEST_DATA_DIR / "general" / "syntax.py")
    assert list(linter.lint_file(filename)) == [
        Error(Location(filename, Position(2, 1)), "Syntax Error")
    ]


def test_check_file_not_found_returns_error() -> None:
    linter = RuleManager.from_rule_names(fix=False)
    filename = str(TEST_DATA_DIR / "general" / "doesnotexist.py")
    assert list(linter.lint_file(filename)) == [
        Error(Location(filename, None), "FileNotFoundError")
    ]


def test_check_file_using_dir_returns_error() -> None:
    linter = RuleManager.from_rule_names(fix=False)
    filename = str(TEST_DATA_DIR / "general")
    assert list(linter.lint_file(filename)) == [
        Error(Location(filename, None), "IsADirectoryError")
    ]


@pytest.mark.parametrize(
    "name, expected", [("frozendict_dict/combined", "frozendict_dict/combined_expected")]
)
def test_fix_rules(name: str, expected: str) -> None:
    filename = f"{name}.py"
    expected_filename = f"{expected}.py"
    fix_rules_test_body(list(Rule.rules.keys()), filename, expected_filename)
