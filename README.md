# Python Linter

Some extra linting rules.

## Install

This works with Python 3.10-3.14.

```bash
uv pip install git+https://github.com/George-Ogden/linter
```

or if you don't use [`uv`](https://github.com/astral-sh/uv/):

```
pip install git+https://github.com/George-Ogden/linter
```

## Usage

```
usage: lint [-h] [--fix] [--include INCLUDE] FILES [FILES ...]

positional arguments:
  FILES

options:
  -h, --help         show this help message and exit
  --fix              Modify files in place.
  --include INCLUDE  Comma separated list of rules to include (defaults to all rules).
```

### Pre-Commit

This is available as a pre-commit hook!

```yaml
- repo: https://github.com/George-Ogden/linter/
  rev: v0.1.2
  hooks:
    - id: lint
      args: [--fix]
```

## Rules

### `string-keyed-dict`

Make string-based dictionaries use `dict` instead of curly braces. For example,

```python
{
  "a": "ascii",
  "r": repr,
  "integer": 15,
}
# is rewritten as
dict(
  a="ascii",
  r=repr,
  integer=15
)
```

This makes it easier to maintain and edit your dictionaries.

## Advanced Usage

### Ignoring Instances

This linter also support `# noqa`.
Put them on the first line they apply.

```python
{  # noqa: string-keyed-dict # put it here!
    "key": "value", # noqa # doesn't work here!
} # noqa # doesn't work here either!
```

## Development

Use the GitHub issue tracker for bugs/feature requests.
When these rules grow up, they want to join [Ruff](https://github.com/astral-sh/ruff)...
