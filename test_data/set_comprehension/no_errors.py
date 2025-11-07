fine = {x for x in range(5)}

list_comp = set([x for x in range(5)])

empty: set[int] = set()

starred: set[int] = set(*(x for x in [[1]]))
