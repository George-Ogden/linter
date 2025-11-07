import frozendict

bad = frozendict.frozendict(dict(keys="values"))

medium = frozendict.frozendict(**bad)

good = frozendict.frozendict(medium)
