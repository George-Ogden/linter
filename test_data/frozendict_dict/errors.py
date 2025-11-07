from frozendict import frozendict

empty: frozendict = frozendict(dict())
empty = frozendict({})

double_dict: dict = dict(dict())

key_value: frozendict = frozendict(
    dict(
        key="value",
        key2="value2",
    )
)

argument = frozendict(dict(key_value))

nested = frozendict(
    dict(
        frozendict(
            dict(
                empty,
            )
        )
    )
)

starred = frozendict(**key_value)

starred_dict = frozendict(**dict(k="v"))

nested_commented: frozendict = frozendict(  # noqa
    dict(
        frozendict(
            {},
        )
    )
)

default_comment = frozendict(dict(frozendict(dict(k="v"))))  # noqa: frozendict-dict
