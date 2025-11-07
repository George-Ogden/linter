from frozendict import frozendict

frozendict_kv = frozendict(
    k="v",
)

frozendict_of_dict = frozendict(d=dict(foo="bar"))

frozendict_curly = frozendict({0: 1, 2: 3})
