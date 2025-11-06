import pytest

from .fullset import fullset


@pytest.mark.parametrize(
    "set1, set2, combined",
    [
        # both empty
        (fullset(), fullset(), fullset()),
        # one empty
        (fullset(), fullset([1]), fullset([1])),
        # basic
        (fullset([1, 2, 3]), fullset([3, 4, 5]), fullset([1, 2, 3, 4, 5])),
        # one full
        (fullset(None), fullset([3, 4, 5]), fullset(None)),
        # both full
        (fullset(None), fullset(None), fullset(None)),
    ],
)
def test_full_set_union(set1: fullset, set2: fullset, combined: fullset) -> None:
    assert set1.union(set2) == combined
    assert set2.union(set1) == combined
