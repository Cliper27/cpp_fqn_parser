from typing import Optional, List, Dict

from .tokenizer import Tokenizer, Token
from .fqn import FQN
from .scope import Scope


class Parser:
    def __init__(self, string: str) -> None:
        self.string: str = string
        self.tokenizer: Tokenizer = Tokenizer(string)
        self.tokens: List[Token] = list(self.tokenizer.get_all_tokens())
        self.cursor: int = len(self.tokens) - 1
        self._has_args: bool = True

    def peek(self) -> Optional[Token]:
        return self.tokens[self.cursor] if self.cursor >= 0 else None

    def consume(self, expected_type: Optional[str] = None) -> Token:
        token: Optional[Token] = self.peek()
        if token is None:
            raise SyntaxError(f"Unexpected end of input, expected: '{expected_type}'")
        if expected_type and token.type_ != expected_type:
            raise SyntaxError(f"Expected token type '{token.type_}' with value '{token.value}'. "
                              f"Expected type: '{expected_type}'")
        self.cursor -= 1
        return token

    def match(self, token_type: str) -> bool:
        token = self.peek()
        return token is not None and token.type_ == token_type

    def parse(self) -> FQN:
        fqn_qualifiers: Dict[str, bool] = self.parse_qualifiers()
        fqn_args: Optional[List[str]] = self.parse_args()
        fqn_template: Optional[str] = self.parse_template()
        fqn_name: str = self.parse_name()
        fqn_scopes: Optional[List[Scope]] = self.parse_scopes()
        fqn_return_type: Optional[str] = self.parse_return_type()
        return FQN(name=fqn_name,
                   full_name=self.string,
                   return_type=fqn_return_type,
                   args=fqn_args,
                   scopes=fqn_scopes,
                   template=fqn_template,
                   constant=fqn_qualifiers["constant"],
                   volatile=fqn_qualifiers["volatile"])

    def parse_qualifiers(self) -> Dict[str, bool]:
        if not self.match("MEMBER"):
            return {"constant": False, "volatile": False}

        token: Token = self.consume("MEMBER")
        constant: bool = token.value == "const"
        volatile: bool = token.value == "volatile"

        if not constant and not volatile:
            raise SyntaxError("FQN has no arguments. "
                              f"Last token is '{token.value}' but should be 'const', 'volatile' or ')'.")

        if not self.match("WHITESPACE"):
            _temp: Optional[Token] = self.peek()
            raise SyntaxError(f"Expected WHITESPACE, found '{_temp.type_ if _temp else None}'")
        self.consume("WHITESPACE")

        if not self.match("MEMBER"):
            return {"constant": constant, "volatile": volatile}

        token = self.consume("MEMBER")
        constant = token.value == "const" if not constant else constant
        volatile = token.value == "volatile" if not volatile else volatile

        if not self.match("WHITESPACE"):
            _temp = self.peek()
            raise SyntaxError(f"Expected WHITESPACE, found '{_temp.type_ if _temp else None}'")
        self.consume("WHITESPACE")

        return {"constant": constant, "volatile": volatile}

    def parse_args(self) -> Optional[List[str]]:
        if not self.match("PARENTHESIS_END"):
            _temp: Optional[Token] = self.peek()
            raise SyntaxError(f"Expected ')', but found {_temp.value if _temp else None}")

        self.consume("PARENTHESIS_END")
        args_list: List[List[str]] = [[]]
        counter: int = 0
        while not self.match("PARENTHESIS_START"):
            if self.match("SEPARATOR"):
                counter += 1
                args_list.append([])
                self.consume("SEPARATOR")
            args_list[counter].append(self.consume().value)
        self.consume("PARENTHESIS_START")

        args: List[str] = [''.join(arg[::-1]) for arg in args_list]

        if len(args) == 1 and not args[0]:
            return None

        return args[::-1]

    def parse_template(self) -> Optional[str]:
        if self.match("WHITESPACE"):
            self.consume("WHITESPACE")

        template: Optional[str] = None
        if self.match("TEMPLATE_END"):
            template = self.parse_nested_templates()

        return template

    def parse_name(self) -> str:
        if self.match("WHITESPACE"):
            self.consume("WHITESPACE")

        if not self.match("MEMBER"):
            _temp: Optional[Token] = self.peek()
            raise SyntaxError(f"Expected 'MEMBER', but found '{_temp.type_ if _temp else 'None'}'")

        name: str = self.consume("MEMBER").value

        return name

    def parse_nested_templates(self) -> str:
        if not self.match("TEMPLATE_END"):
            _temp: Optional[Token] = self.peek()
            raise SyntaxError(f"Expected '>', but found '{_temp.value if _temp else 'None'}'")

        tokens: List[str] = [self.consume("TEMPLATE_END").value]
        depth: int = 1
        while depth > 0:
            token: Token = self.consume()
            tokens.append(token.value)
            if token.type_ == "TEMPLATE_END":
                depth += 1
            elif token.type_ == "TEMPLATE_START":
                depth -= 1

        return ''.join(tokens[::-1])

    def parse_scopes(self) -> Optional[List[Scope]]:
        if not self.match("SCOPE"):
            return None

        scopes: List[Scope] = []

        while not self.match("WHITESPACE") and self.peek():
            self.consume("SCOPE")
            template: Optional[str] = self.parse_nested_templates() if self.match("TEMPLATE_END") else None
            token: Token = self.consume("MEMBER")

            scopes.append(Scope(token.value, template))

        return scopes[::-1]

    def parse_return_type(self) -> Optional[str]:
        if self.match("WHITESPACE"):
            self.consume("WHITESPACE")

        if not self.peek():
            return None

        return_type: List[str] = []
        while self.peek():
            token = self.consume()
            return_type.append(token.value)

        return ''.join(return_type[::-1])
