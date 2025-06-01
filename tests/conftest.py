from typing import List

import pytest

from src.token import Token
from src.fqn import FQN
from src.scope import Scope


@pytest.fixture
def simple_fqn_input() -> str:
    return "one::two::three()"


@pytest.fixture
def simple_tokenizer_expected() -> List[Token]:
    return [
        Token('MEMBER', 'one'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'two'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'three'),
        Token('PARENTHESIS_START', '('),
        Token('PARENTHESIS_END', ')'),
    ]


@pytest.fixture
def simple_parser_expected():
    scopes = [
        Scope(name="one", template=None),
        Scope(name="two", template=None)
    ]
    return FQN(name="three",
               full_name="one::two::three()",
               return_type=None,
               args=None,
               scopes=scopes,
               template=None,
               constant=False,
               volatile=False)


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