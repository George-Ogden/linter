flat = set(x for x in range(5))

bracketed = set((y for y in range(6)))  # noqa: UP034

multiline = set(
    (y + 1 for y in [1, 2, 3]),
)

nested_set_comp = list(set({z for z in range(len(set(u for u in range(6))))}))
