multiline = set(  # noqa: set-comprehension
    (x + 1 for x in [1, 2, 3]),
)

multiline = set(
    (y + 1 for y in [1, 2, 3]),  # noqa: wrong line
)

multiline = set(
    (z + 1 for z in [1, 2, 3]),
)  # noqa: set-comprehension # wrong line

nested = set(
    (x for x in set(y for y in [None])),  # noqa: set-comprehension
)
