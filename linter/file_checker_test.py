from .feedback import Error
from .position import Location, Position
from .rule_manager import RuleManager
from .test_utils import TEST_DATA_DIR


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
