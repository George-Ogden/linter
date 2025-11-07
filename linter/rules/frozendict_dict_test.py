import os

import pytest

from ..test_utils import check_rules_test_body, fix_rules_test_body


@pytest.mark.parametrize(
    "name, expected_positions",
    [
        ("empty", []),
        (
            "errors",
            [(3, 21), (4, 9), (8, 25), (15, 12), (17, 10), (19, 9), (27, 11), (29, 16), (33, 9)],
        ),
        ("combined", [(3, 5)]),
        ("indirect", [(3, 7), (5, 10)]),
        ("no_errors", []),
    ],
)
def test_check_frozendict_dict(name: str, expected_positions: list[tuple[int, int]]) -> None:
    filename = os.path.join("frozendict_dict", f"{name}.py")
    check_rules_test_body(["frozendict-dict"], filename, expected_positions)


@pytest.mark.parametrize(
    "name, expected",
    [("empty", "empty"), ("errors", "expected"), ("indirect", "indirect_expected")],
)
def test_fix_frozendict_dict(name: str, expected: str) -> None:
    filename = os.path.join("frozendict_dict", f"{name}.py")
    expected_filename = os.path.join("frozendict_dict", f"{expected}.py")
    fix_rules_test_body(["frozendict-dict"], filename, expected_filename)
