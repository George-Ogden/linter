flat = {x for x in range(5)}

bracketed = {y for y in range(6)}  # noqa: UP034

multiline = {
    y + 1 for y in [1, 2, 3]
}

nested_set_comp = list({z for z in range(len({u for u in range(6)}))})
