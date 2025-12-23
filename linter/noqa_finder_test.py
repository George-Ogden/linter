import pytest

from .fullset import fullset
from .noqa_finder import IgnoredLines, NoqaFinder
from .test_utils import TEST_DATA_DIR


@pytest.mark.parametrize(
    "comment, expected_codes",
    [
        # random comment
        ("# random comment", []),
        # not noqa
        ("# unoqa", []),
        # full noqa
        ("#noqa", None),
        # full noqa with colon
        ("# noqa:", None),
        # noqa_ with extra space
        ("# noqa :", None),
        # full noqa extra text
        ("# noqa and other things", None),
        # full noqa with other directives
        ("# noqa # type: ignore", None),
        # full noqa with other noqas
        ("# noqa # noqa: RUF100", None),
        # individual noqa
        ("# noqa: RUF100 ", ["RUF100"]),
        # individual without spaces
        ("# noqa:dict_list-set:", ["dict_list-set:"]),
        # multiple noqas
        ("# noqa: A10, B4 ", ["A10", "B4"]),
        # multiple noqas with extra commas
        ("# noqa: A10, , B4 ", ["A10", "B4"]),
        # multiple noqas without spaces
        ("# noqa:A10:0,B4-,C_8", ["A10:0", "B4-", "C_8"]),
        # multiple split noqas
        ("# noqa: A # noqa: B # type: ignore # noqa: C,D", ["A", "B", "C", "D"]),
        # not first noqa
        ("# blah noqa: A", ["A"]),
        # duplicated noqa
        ("# noqa: A, B # noqa: B, C", ["A", "B", "C"]),
        # noqa_ extra spaces
        ("# noqa : A B", ["A"]),
    ],
)
def test_parse_comment(comment: str, expected_codes: list[str] | None) -> None:
    assert NoqaFinder.parse_comment(comment) == fullset(expected_codes)


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("empty", {}),
        ("no_noqas", {}),
        (
            "many_noqas",
            {
                1: fullset(["import"]),
                2: fullset(None),
                5: fullset(None),
                9: fullset(["bar", "baz"]),
                10: fullset(["foo", "baz"]),
            },
        ),
    ],
)
def test_find_noqas(filename: str, expected: IgnoredLines) -> None:
    with open(TEST_DATA_DIR / "noqa" / f"{filename}.py") as f:
        lines = f.readlines()

    assert NoqaFinder.parse_lines(iter(lines)) == expected
