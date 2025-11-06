from collections.abc import Iterable
import functools
import re
import token
import tokenize
from typing import cast

from .fullset import fullset

type IgnoredLines = dict[int, fullset[str]]


class NoqaFinder:
    @classmethod
    def parse_lines(cls, lines: Iterable[str]) -> IgnoredLines:
        comments = cls.get_comments(lines)
        return {line: cls.parse_comment(comment) for line, comment in comments}

    @classmethod
    def get_comments(cls, lines: Iterable[str]) -> Iterable[tuple[int, str]]:
        tokens = tokenize.generate_tokens(functools.partial(next, iter(lines)))
        return ((tok.start[0], tok.string) for tok in tokens if tok.type == token.COMMENT)

    @classmethod
    def parse_comment(cls, comment: str) -> fullset[str]:
        comment_sections = comment.split("#")
        return functools.reduce(
            fullset.union,
            (
                cls.parse_comment_section(comment_section)
                for comment_section in comment_sections
                if comment_section.strip()
            ),
            cast(fullset[str], fullset()),
        )

    @classmethod
    def parse_comment_section(cls, section: str) -> fullset[str]:
        pattern = r"\bnoqa\s*(:(.*))?"
        match = re.search(pattern, section)
        if match is None:
            return fullset()
        return cls.parse_code_section(match.group(2) or "")

    @classmethod
    def parse_code_section(cls, section: str) -> fullset[str]:
        section = section.strip()
        codes: fullset[str] = fullset()
        for potential_code in section.split(","):
            match potential_code.strip().split(maxsplit=1):
                case [code, *extra]:
                    codes.add(code)
                    if extra:
                        break
        if codes:
            return codes
        return fullset(None)
