from typing import List

from src.tokenizer import Tokenizer, Token


def test_simple_fqn(simple_fqn_input: str, simple_fqn_expected: List[Token]) -> None:
    tokenizer: Tokenizer = Tokenizer(simple_fqn_input)
    result: List[Token] = list(tokenizer.get_all_tokens())
    assert result == simple_fqn_expected


def test_fqn(fqn_input: str, fqn_expected: List[Token]) -> None:
    tokenizer: Tokenizer = Tokenizer(fqn_input)
    result: List[Token] = list(tokenizer.get_all_tokens())
    assert result == fqn_expected
