import os

import pytest

from ..test_utils import check_rules_test_body


@pytest.mark.parametrize(
    "name, expected_positions",
    [
        ("empty", []),
        ("errors", [(1, 5), (4, 5), (5, 5), (6, 21), (6, 5), (7, 5)]),
        ("keywords", [(1, 10)]),
        ("no_errors", []),
        ("commented", [(9, 5), (13, 5), (19, 5), (23, 5), (27, 5)]),
    ],
)
def test_check_string_keyed_dict(name: str, expected_positions: list[tuple[int, int]]) -> None:
    filename = os.path.join("string_keyed_dict", f"{name}.py")
    check_rules_test_body(["string-keyed-dict"], filename, expected_positions)
