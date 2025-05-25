from dataclasses import dataclass
from typing import Optional, Union, List, Dict

from tokenizer import Tokenizer, Token


@dataclass
class Scope:
    name: str
    template: Optional[str] = None


@dataclass
class ReturnType:
    name: str
    constant: bool = False
    volatile: bool = False
    pointer: bool = False
    reference: bool = False
    template: Optional[str] = None


@dataclass
class FQN:
    name: str
    full_name: str
    return_type: Optional[ReturnType] = None
    args: Optional[List[str]] = None
    scopes: Optional[List[Scope]] = None
    template: Optional[str] = None
    constant: bool = False
    volatile: bool = False


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
        fqn_args: List[str] = self.parse_args()
        fqn_template: Optional[str] = self.parse_template()
        fqn_name: str = self.parse_name()
        fqn_scopes: Optional[List[Scope]] = self.parse_scopes()  # TODO
        return fqn_qualifiers, fqn_args, fqn_template, fqn_name, fqn_scopes  # TODO

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

    def parse_args(self) -> List[str]:
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

    def parse_scopes(self):
        # TODO
        ...


    # def parse_return_type(self) -> ReturnType:
    #     constant = False
    #     volatile = False
    #     pointer = False
    #     reference = False
    #
    #     if not self.match("MEMBER"):
    #         raise SyntaxError(f"First token must be a MEMBER, "
    #                           f"but '{self.peek().type_ if self.peek() else 'None'}' found.")
    #
    #     token = self.consume("MEMBER")
    #     constant = token.value == "const"
    #     volatile = token.value == "volatile"
    #
    #
    #     return ReturnType(
    #         name=name,
    #         constant=constant,
    #         volatile=volatile,
    #         pointer=pointer,
    #         reference=reference,
    #         template=template_str
    #     )


# def parse_return_type(self) -> ReturnType:
#     constant = False
#     volatile = False
#     pointer = False
#     reference = False
#
#     # handle leading qualifiers
#     while self.match("CONSTANT") or self.match("VOLATILE"):
#         if self.match("CONSTANT"):
#             self.consume("CONSTANT")
#             constant = True
#         elif self.match("VOLATILE"):
#             self.consume("VOLATILE")
#             volatile = True
#
#     # parse scoped name (e.g., std::vector)
#     name_parts = [self.consume("MEMBER").value]
#     while self.match("SCOPE"):
#         self.consume("SCOPE")
#         name_parts.append(self.consume("MEMBER").value)
#     name = "::".join(name_parts)
#
#     # optional template
#     template_str = None
#     if self.match("TEMPLATE_START"):
#         start_pos = self.pos
#         depth = 0
#         while self.pos < len(self.tokens):
#             if self.match("TEMPLATE_START"):
#                 depth += 1
#             elif self.match("TEMPLATE_END"):
#                 depth -= 1
#                 if depth == 0:
#                     self.pos += 1  # consume final >
#                     break
#             self.pos += 1
#         template_str = "..."  # placeholder for full parser
#
#     # pointer/reference qualifiers
#     while self.match("POINTER") or self.match("REFERENCE"):
#         if self.match("POINTER"):
#             self.consume("POINTER")
#             pointer = True
#         elif self.match("REFERENCE"):
#             self.consume("REFERENCE")
#             reference = True
#
#     return ReturnType(
#         name=name,
#         constant=constant,
#         volatile=volatile,
#         pointer=pointer,
#         reference=reference,
#         template=template_str
#     )


if __name__ == '__main__':
    fqn = r"int one_3hello0::tconstwo<mytemplate>::three<Test::type<T * >::Hello>(const four &, int a) volatile"
    parser = Parser(fqn)
    parsed_fqn = parser.parse()
    print(fqn)
