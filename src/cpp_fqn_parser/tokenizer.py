import re
from typing import Optional, Pattern, Match, List, Tuple
from collections.abc import Iterator

from .token import Token

OPERATORS: List[str] = ['+', '-', '/', '*', '%',
                        '++', '--',
                        '<', '>', '<=', '>=', '==', '!=',
                        '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=',
                        '<<', '>>', '&', '^', '~', '|',
                        '&&', '||', '!',
                        '->', '[]',
                        '=',
                        '()', ',']

SORTED_OPERATORS: List[str] = sorted(OPERATORS, key=len, reverse=True)

_OPERATOR_PREFIX_RE = re.compile(r"^operator\b\s*")

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

    Private Attributes:
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

        token = self.get_operator(string)
        if token:
            return token

        for pattern, token_type in _SPEC:
            token_value: Optional[str] = self._match(pattern, string)
            if token_value is not None:
                return Token(token_type, token_value)

        raise SyntaxError(f"Unexpected token '{string[0]}'")

    def get_operator(self, string: str) -> Optional[Token]:
        """
        Attempts to match and extract a C++ operator overload token from the beginning of the input string.

        This method detects the 'operator' keyword as a whole word, optionally followed by whitespace
        and a valid C++ operator symbol (e.g., '==', '[]', '+', etc.). If a match is found, it consumes
        the corresponding characters from the input and returns an OPERATOR token. If only the 'operator'
        keyword is matched without a valid symbol, a MEMBER token for 'operator' is returned.

        Args:
            string (str): The remaining input string to check for an operator overload.

        Returns:
            Optional[Token]: A Token of type 'OPERATOR' or 'MEMBER' if matched, or None if no match is found.
        """
        match = _OPERATOR_PREFIX_RE.match(string)
        if not match:
            return None

        prefix_len = match.end()
        remainder = string[prefix_len:]
        op_symbol = _match_operator_symbol(remainder)
        if op_symbol:
            self.__cursor += prefix_len + len(op_symbol)
            return Token("OPERATOR", f"operator{op_symbol}")
        else:
            self.__cursor += prefix_len
            return Token("MEMBER", "operator")

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


def _match_operator_symbol(string: str) -> Optional[str]:
    """
    Attempts to match a valid C++ operator symbol at the start of the given string.

    The function checks whether the input string begins with any of the predefined C++
    operator overload symbols (e.g., '==', '+', '[]', '->', etc.), prioritizing longer
    matches first (e.g., '>>=' before '>').

    Args:
        string (str): The string to match against known operator symbols.

    Returns:
        Optional[str]: The matched operator symbol if found, otherwise None.
    """
    for op in SORTED_OPERATORS:
        if string.startswith(op):
            return op
    return None
