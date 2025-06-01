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
    """
    A simple tokenizer that converts a string into a stream of tokens based on predefined patterns.

    Attributes:
        string (str): The input string to tokenize.
        __cursor (int): Internal cursor tracking the current position in the input string.
    """
    def __init__(self, string: str) -> None:
        """
        Initializes the tokenizer with the input string.

        Args:
            string (str): The string to be tokenized.
        """
        self.string: str = string
        self.__cursor: int = 0

    def _has_more_tokens(self) -> bool:
        """
        Checks whether there are more tokens to extract.

        Returns:
            bool: True if there are unprocessed characters in the input string.
        """
        return self.__cursor < len(self.string)

    def get_next_token(self) -> Optional[Token]:
        """
        Extracts the next token from the input string.

        Returns:
            Optional[Token]: The next token, or None if the end of input is reached.

        Raises:
            SyntaxError: If an unrecognized token is encountered.
        """
        if not self._has_more_tokens():
            return None

        string: str = self.string[self.__cursor:]

        for pattern, token_type in _SPEC:
            token_value: Optional[str] = self._match(pattern, string)

            if token_value is None:
                continue

            return Token(token_type, token_value)

        raise SyntaxError(f"Unexpected token '{string[0]}'")

    def _match(self, pattern: str | Pattern[str], string: str) -> Optional[str]:
        """
        Tries to match a regex pattern at the start of the input string.

        Args:
            pattern (str | Pattern[str]): The regex pattern to match.
            string (str): The remaining string to match against.

        Returns:
            Optional[str]: The matched string, or None if no match was found.
        """
        matched: Optional[Match] = re.match(pattern, string)
        if matched is not None:
            token: str = matched[0]
            self.__cursor += len(token)
            return token
        return None

    def get_all_tokens(self) -> Iterator[Token]:
        """
        Tokenizes the entire input string.

        Yields:
            Iterator[Token]: A generator of Token objects in the order they appear.
        """
        self.__cursor = 0
        while token := self.get_next_token():
            yield token
