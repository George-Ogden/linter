import frozendict

bad = frozendict.frozendict(keys="values")

medium = frozendict.frozendict(bad)

good = frozendict.frozendict(medium)
