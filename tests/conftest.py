from typing import List

import pytest

from src.tokenizer import Token


@pytest.fixture
def simple_fqn_input() -> str:
    return "one::two::three"


@pytest.fixture
def simple_fqn_expected() -> List[Token]:
    return [
        Token('MEMBER', 'one'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'two'),
        Token('SCOPE', '::'),
        Token('MEMBER', 'three')
    ]


@pytest.fixture
def fqn_input() -> str:
    return "int one_3hello0::tconstwo<mytemplate>::three(const four &) volatile"


@pytest.fixture
def fqn_expected() -> List[Token]:
    return [
        Token('MEMBER',             'int'),
        Token('WHITESPACE',         ' '),
        Token('MEMBER',             'one_3hello0'),
        Token('SCOPE',              '::'),
        Token('MEMBER',             'tconstwo'),
        Token('TEMPLATE_START',     '<'),
        Token('MEMBER',             'mytemplate'),
        Token('TEMPLATE_END',       '>'),
        Token('SCOPE',              '::'),
        Token('MEMBER',             'three'),
        Token('PARENTHESIS_START',  '('),
        Token('MEMBER',             'const'),
        Token('WHITESPACE',         ' '),
        Token('MEMBER',             'four'),
        Token('WHITESPACE',         ' '),
        Token('REFERENCE',          '&'),
        Token('PARENTHESIS_END',    ')'),
        Token('WHITESPACE',         ' '),
        Token('MEMBER',             'volatile')
    ]
