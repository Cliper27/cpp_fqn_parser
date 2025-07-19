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


def test_operator_fqn(operator_fqn_input: str, operator_tokenizer_expected: List[Token]) -> None:
    tokenizer: Tokenizer = Tokenizer(operator_fqn_input)
    result: List[Token] = list(tokenizer.get_all_tokens())
    assert result == operator_tokenizer_expected


def test_operator_fqn_2(operator_fqn_input_2: str, operator_tokenizer_expected_2: List[Token]) -> None:
    tokenizer: Tokenizer = Tokenizer(operator_fqn_input_2)
    result: List[Token] = list(tokenizer.get_all_tokens())
    assert result == operator_tokenizer_expected_2
