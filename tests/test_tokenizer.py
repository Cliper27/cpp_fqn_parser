from typing import List

from src.tokenizer import Tokenizer
from src.token import Token


def test_simple_fqn(simple_fqn_input: str, simple_tokenizer_expected: List[Token]) -> None:
    tokenizer: Tokenizer = Tokenizer(simple_fqn_input)
    result: List[Token] = list(tokenizer.get_all_tokens())
    assert result == simple_tokenizer_expected


def test_fqn(fqn_input: str, tokenizer_expected: List[Token]) -> None:
    tokenizer: Tokenizer = Tokenizer(fqn_input)
    result: List[Token] = list(tokenizer.get_all_tokens())
    assert result == tokenizer_expected
