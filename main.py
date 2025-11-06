import argparse
from collections.abc import Sequence
import sys
from typing import NoReturn

from linter.config import LinterConfig
from linter.rule import Rule


def rule_names_from_csv(csv: str) -> list[str]:
    rules = csv.split(",")
    for rule in rules:
        if rule not in Rule.rules:
            raise argparse.ArgumentTypeError(f"Invalid rule: {rule}")
    return rules


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", metavar="FILES")
    parser.add_argument("--fix", action="store_true", help="Modify files in place.")
    parser.add_argument(
        "--include",
        help="Comma separated list of rules to include (defaults to all rules).",
        type=rule_names_from_csv,
        default=list(Rule.rules),
    )
    return parser.parse_args()


def main(args: argparse.Namespace) -> bool:
    filenames: Sequence[str] = args.files
    fix: bool = args.fix
    include: list[str] = args.include
    config = LinterConfig(included_rule_names=include, fix=fix, filenames=filenames)
    return bool(config.run())


def main_cli() -> NoReturn:
    args = parse_args()
    sys.exit(main(args))


if __name__ == "__main__":
    main_cli()
