from pathlib import Path
import json
from typing import List

import pytest

from src.cpp_fqn_parser import Token, FQN, Scope


def pytest_generate_tests(metafunc):
    if "fqn_dict" in metafunc.fixturenames:
        path = Path(__file__).parent.parent / "test_data" / "fqns.json"
        with path.open() as f:
            fqns = json.load(f)
        metafunc.parametrize("fqn_dict", fqns)


@pytest.fixture
def fqn_input() -> str:
    return "int one_3hello0::tconstwo<mytemplate>::three(const four &) volatile"


@pytest.fixture
def tokenizer_expected() -> List[Token]:
    return [
        Token('MEMBER', 'int'),
        Token('WHITESPACE', ' '),
        Token('MEMBER', 'one_3hello0'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'tconstwo'),
        Token('TEMPLATE_START', '<'),
        Token('MEMBER', 'mytemplate'),
        Token('TEMPLATE_END', '>'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'three'),
        Token('PARENTHESIS_START', '('),
        Token('MEMBER', 'const'),
        Token('WHITESPACE', ' '),
        Token('MEMBER', 'four'),
        Token('WHITESPACE', ' '),
        Token('REFERENCE', '&'),
        Token('PARENTHESIS_END', ')'),
        Token('WHITESPACE', ' '),
        Token('MEMBER', 'volatile')
    ]


@pytest.fixture
def parser_expected():
    scopes = [
        Scope(name="one_3hello0", template=None),
        Scope(name="tconstwo", template="<mytemplate>")
    ]
    return FQN(name="three",
               full_name="int one_3hello0::tconstwo<mytemplate>::three(const four &) volatile",
               return_type="int",
               args=["const four &"],
               scopes=scopes,
               template=None,
               constant=False,
               volatile=True)


@pytest.fixture
def operator_fqn_input() -> str:
    return "one::two::operator*()"


@pytest.fixture
def operator_tokenizer_expected() -> List[Token]:
    return [
        Token('MEMBER', 'one'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'two'),
        Token('SCOPE', '::'),
        Token('OPERATOR', 'operator*'),
        Token('PARENTHESIS_START', '('),
        Token('PARENTHESIS_END', ')'),
    ]


@pytest.fixture
def operator_fqn_input_2() -> str:
    return "one::two::operator []()"


@pytest.fixture
def operator_tokenizer_expected_2() -> List[Token]:
    return [
        Token('MEMBER', 'one'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'two'),
        Token('SCOPE', '::'),
        Token('OPERATOR', 'operator[]'),
        Token('PARENTHESIS_START', '('),
        Token('PARENTHESIS_END', ')'),
    ]


@pytest.fixture
def parser_operator_expected():
    scopes = [
        Scope(name="one", template=None),
        Scope(name="two", template=None)
    ]
    return FQN(name="operator*",
               full_name="one::two::operator*()",
               return_type=None,
               args=None,
               scopes=scopes,
               template=None,
               constant=False,
               volatile=False)


@pytest.fixture
def parser_operator_expected_2():
    scopes = [
        Scope(name="one", template=None),
        Scope(name="two", template=None)
    ]
    return FQN(name="operator[]",
               full_name="one::two::operator []()",
               return_type=None,
               args=None,
               scopes=scopes,
               template=None,
               constant=False,
               volatile=False)
