from src.cpp_fqn_parser import Parser, FQN


def test_tokenizer_fqn(fqn_dict: dict):
    parser: Parser = Parser(fqn_dict["fqn"])
    result: FQN = parser.parse()
    expected = FQN.from_dict(fqn_dict["parser"])
    assert result == expected


def test_fqn(fqn_input: str, parser_expected: FQN) -> None:
    parser: Parser = Parser(fqn_input)
    result: FQN = parser.parse()
    assert result == parser_expected


def test_operator_fqn(operator_fqn_input: str, parser_operator_expected: FQN) -> None:
    parser: Parser = Parser(operator_fqn_input)
    result: FQN = parser.parse()
    assert result == parser_operator_expected


def test_operator_fqn_2(operator_fqn_input_2: str, parser_operator_expected_2: FQN) -> None:
    parser: Parser = Parser(operator_fqn_input_2)
    result: FQN = parser.parse()
    assert result == parser_operator_expected_2
