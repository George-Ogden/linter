# noqa: import
from bar import foo  # type: ignore  # noqa


def foo() -> None:  # type: ignore # noqa
    ...


def bar() -> None:  # noqa: bar, baz
    foo()  # noqa: foo # noqa: baz
