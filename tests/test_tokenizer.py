from typing import List

from src.cpp_fqn_parser import Tokenizer, Token


def test_tokenizer_fqn(fqn_dict: dict):
    tokenizer: Tokenizer = Tokenizer(fqn_dict["fqn"])
    result: List[Token] = list(tokenizer.get_all_tokens())
    expected = [Token.from_dict(token)
                for token in fqn_dict["tokens"]]
    assert result == expected
