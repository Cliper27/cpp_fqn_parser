from src.cpp_fqn_parser import Parser, FQN


def test_tokenizer_fqn(fqn_dict: dict):
    parser: Parser = Parser(fqn_dict["fqn"])
    result: FQN = parser.parse()
    expected = FQN.from_dict(fqn_dict["parser"])
    assert result == expected
