import os

import pytest

from ..test_utils import check_rules_test_body, fix_rules_test_body


@pytest.mark.parametrize(
    "name, expected_positions",
    [
        ("empty", []),
        ("errors", [(1, 1), (4, 6), (7, 1), (9, 1), (10, 1)]),
        ("no_errors", []),
        ("commented", [(4, 6)]),
        ("comprehensions", [(1, 1), (2, 1), (3, 1)]),
    ],
)
def test_check_str_join(name: str, expected_positions: list[tuple[int, int]]) -> None:
    filename = os.path.join("str_join", f"{name}.py")
    check_rules_test_body(["str-join"], filename, expected_positions)


@pytest.mark.parametrize(
    "name, expected",
    [("empty", "empty"), ("errors", "expected"), ("comprehensions", "comprehensions_expected")],
)
def test_fix_str_join(name: str, expected: str) -> None:
    filename = os.path.join("str_join", f"{name}.py")
    expected_filename = os.path.join("str_join", f"{expected}.py")
    fix_rules_test_body(["str-join"], filename, expected_filename)
