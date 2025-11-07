from frozendict import frozendict

empty: frozendict = frozendict()
empty = frozendict()

double_dict: dict = dict(dict())

key_value: frozendict = frozendict(
        key="value",
        key2="value2",
    )

argument = frozendict(key_value)

nested = frozendict(
        frozendict(
                empty,
            )
    )

starred = frozendict(key_value)

starred_dict = frozendict(k="v")

nested_commented: frozendict = frozendict(  # noqa
    dict(
        frozendict()
    )
)

default_comment = frozendict(dict(frozendict(dict(k="v"))))  # noqa: frozendict-dict
