from src.parser import Parser
from src.fqn import FQN


def test_simple_fqn(simple_fqn_input: str, simple_parser_expected: FQN) -> None:
    parser: Parser = Parser(simple_fqn_input)
    result: FQN = parser.parse()
    assert result == simple_parser_expected


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
