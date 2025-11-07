import os

import pytest

from ..test_utils import check_rules_test_body, fix_rules_test_body


@pytest.mark.parametrize(
    "name, expected_positions",
    [
        ("empty", []),
        ("errors", [(1, 8), (3, 13), (5, 13), (9, 24), (9, 50)]),
        ("no_errors", []),
        ("commented", [(5, 13), (9, 13), (13, 10)]),
    ],
)
def test_check_set_comprehension(name: str, expected_positions: list[tuple[int, int]]) -> None:
    filename = os.path.join("set_comprehension", f"{name}.py")
    check_rules_test_body(["set-comprehension"], filename, expected_positions)


@pytest.mark.parametrize("name, expected", [("errors", "expected")])
def test_fix_set_comprehension(name: str, expected: str) -> None:
    filename = os.path.join("set_comprehension", f"{name}.py")
    expected_filename = os.path.join("set_comprehension", f"{expected}.py")
    fix_rules_test_body(["set-comprehension"], filename, expected_filename)
