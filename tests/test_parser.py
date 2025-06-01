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
