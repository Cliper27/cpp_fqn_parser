import re
from typing import Optional, Pattern, Match, List, Tuple
from collections.abc import Iterator

from .token import Token


_SPEC: List[Tuple[Pattern[str], str]] = [
    (re.compile(r"^\s+"), "WHITESPACE"),
    (re.compile(r"^::"), "SCOPE"),
    (re.compile(r"^<"), "TEMPLATE_START"),
    (re.compile(r"^>"), "TEMPLATE_END"),
    (re.compile(r"^\("), "PARENTHESIS_START"),
    (re.compile(r"^\)"), "PARENTHESIS_END"),
    (re.compile(r"^\*"), "POINTER"),
    (re.compile(r"^&"), "REFERENCE"),
    (re.compile(r"^,"), "SEPARATOR"),
    (re.compile(r"^[a-zA-Z_]\w*"), "MEMBER"),
]


class Tokenizer:
    def __init__(self, string: str) -> None:
        self.string: str = string
        self.cursor: int = 0

    def is_eof(self) -> bool:
        return self.cursor == len(self.string)

    def has_more_tokens(self) -> bool:
        return self.cursor < len(self.string)

    def get_next_token(self) -> Optional[Token]:
        if not self.has_more_tokens():
            return None

        string: str = self.string[self.cursor:]

        for pattern, token_type in _SPEC:
            token_value: Optional[str] = self._match(pattern, string)

            if token_value is None:
                continue

            return Token(token_type, token_value)

        raise SyntaxError(f"Unexpected token '{string[0]}'")

    def _match(self, pattern: str | Pattern[str], string: str) -> Optional[str]:
        matched: Optional[Match] = re.match(pattern, string)
        if matched is not None:
            token: str = matched[0]
            self.cursor += len(token)
            return token
        return None

    def get_all_tokens(self) -> Iterator[Token]:
        self.cursor = 0
        while token := self.get_next_token():
            yield token
