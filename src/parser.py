from typing import Optional, List, Dict

from .tokenizer import Tokenizer, Token
from .fqn import FQN
from .scope import Scope


class Parser:
    """
    Parses a string representation of a fully qualified name (FQN) into a structured FQN object.

    This parser consumes tokens produced by a `Tokenizer` and reconstructs:
      - the symbol name
      - its argument list
      - template definitions
      - qualifier flags (const, volatile)
      - return type
      - and any enclosing scopes

    Attributes:
        string (str): The original input string.
        tokenizer (Tokenizer): Tokenizer instance processing the input.
        tokens (List[Token]): All parsed tokens from the input.
        __cursor (int): Current index in the token list (reverse parsing).
    """
    def __init__(self, string: str) -> None:
        """
        Initializes the parser and tokenizes the input string.

        Args:
            string (str): The string to parse.
        """
        self.string: str = string
        self.tokenizer: Tokenizer = Tokenizer(string)
        self.tokens: List[Token] = list(self.tokenizer.get_all_tokens())
        self.__cursor: int = len(self.tokens) - 1

    def _peek(self) -> Optional[Token]:
        """
        Looks at the current token without consuming it.

        Returns:
            Optional[Token]: The current token, or None if at the start.
        """
        return self.tokens[self.__cursor] if self.__cursor >= 0 else None

    def _consume(self, expected_type: Optional[str] = None) -> Token:
        """
        Consumes and returns the current token, optionally verifying its type.

        Args:
            expected_type (Optional[str]): Expected token type (if any).

        Returns:
            Token: The consumed token.

        Raises:
            SyntaxError: If the token type doesn't match or input ends unexpectedly.
        """
        token: Optional[Token] = self._peek()
        if token is None:
            raise SyntaxError(f"Unexpected end of input, expected: '{expected_type}'")
        if expected_type and token.type_ != expected_type:
            raise SyntaxError(f"Expected token type '{token.type_}' with value '{token.value}'. "
                              f"Expected type: '{expected_type}'")
        self.__cursor -= 1
        return token

    def _match(self, token_type: str) -> bool:
        """
        Checks if the current token matches a given type.

        Args:
            token_type (str): The token type to check.

        Returns:
            bool: True if the current token matches the type, False otherwise.
        """
        token = self._peek()
        return token is not None and token.type_ == token_type

    def parse(self) -> FQN:
        """
        Parses the entire input string into an FQN object.

        Returns:
            FQN: The parsed fully qualified name structure.
        """
        fqn_qualifiers: Dict[str, bool] = self._parse_qualifiers()
        fqn_args: Optional[List[str]] = self._parse_args()
        fqn_template: Optional[str] = self._parse_template()
        fqn_name: str = self._parse_name()
        fqn_scopes: Optional[List[Scope]] = self._parse_scopes()
        fqn_return_type: Optional[str] = self._parse_return_type()
        return FQN(name=fqn_name,
                   full_name=self.string,
                   return_type=fqn_return_type,
                   args=fqn_args,
                   scopes=fqn_scopes,
                   template=fqn_template,
                   constant=fqn_qualifiers["constant"],
                   volatile=fqn_qualifiers["volatile"])

    def _parse_qualifiers(self) -> Dict[str, bool]:
        """
        Parses trailing qualifiers like 'const' and 'volatile'.

        Returns:
            Dict[str, bool]: A dictionary with boolean flags: {'constant': bool, 'volatile': bool}
        """
        if not self._match("MEMBER"):
            return {"constant": False, "volatile": False}

        token: Token = self._consume("MEMBER")
        constant: bool = token.value == "const"
        volatile: bool = token.value == "volatile"

        if not constant and not volatile:
            raise SyntaxError("FQN has no arguments. "
                              f"Last token is '{token.value}' but should be 'const', 'volatile' or ')'.")

        if not self._match("WHITESPACE"):
            _temp: Optional[Token] = self._peek()
            raise SyntaxError(f"Expected WHITESPACE, found '{_temp.type_ if _temp else None}'")
        self._consume("WHITESPACE")

        if not self._match("MEMBER"):
            return {"constant": constant, "volatile": volatile}

        token = self._consume("MEMBER")
        constant = token.value == "const" if not constant else constant
        volatile = token.value == "volatile" if not volatile else volatile

        if not self._match("WHITESPACE"):
            _temp = self._peek()
            raise SyntaxError(f"Expected WHITESPACE, found '{_temp.type_ if _temp else None}'")
        self._consume("WHITESPACE")

        return {"constant": constant, "volatile": volatile}

    def _parse_args(self) -> Optional[List[str]]:
        """
        Parses function arguments inside parentheses.

        Returns:
            Optional[List[str]]: The list of argument strings, or None if no arguments found.
        """
        if not self._match("PARENTHESIS_END"):
            return None

        self._consume("PARENTHESIS_END")
        args_list: List[List[str]] = [[]]
        counter: int = 0
        while not self._match("PARENTHESIS_START"):
            if self._match("SEPARATOR"):
                counter += 1
                args_list.append([])
                self._consume("SEPARATOR")
            args_list[counter].append(self._consume().value)
        self._consume("PARENTHESIS_START")

        args: List[str] = [''.join(arg[::-1]) for arg in args_list]

        if len(args) == 1 and not args[0]:
            return None

        return args[::-1]

    def _parse_template(self) -> Optional[str]:
        """
        Parses template type parameters if present.

        Returns:
            Optional[str]: The raw template string, or None.
        """
        if self._match("WHITESPACE"):
            self._consume("WHITESPACE")

        template: Optional[str] = None
        if self._match("TEMPLATE_END"):
            template = self._parse_nested_templates()

        return template

    def _parse_name(self) -> str:
        """
        Parses the function or symbol name.

        Returns:
            str: The unqualified name.

        Raises:
            SyntaxError: If a valid member token is not found.
        """
        if self._match("WHITESPACE"):
            self._consume("WHITESPACE")

        if self._match("OPERATOR"):
            name: str = self._consume("OPERATOR").value
            return name
        elif not self._match("MEMBER"):
            _temp: Optional[Token] = self._peek()
            raise SyntaxError(f"Expected 'MEMBER', but found '{_temp.type_ if _temp else 'None'}'")

        name = self._consume("MEMBER").value
        return name

    def _parse_nested_templates(self) -> str:
        """
        Parses a possibly nested set of template tokens.

        Returns:
            str: The raw template string (reversed back to original order).

        Raises:
            SyntaxError: If improper template structure is found.
        """
        if not self._match("TEMPLATE_END"):
            _temp: Optional[Token] = self._peek()
            raise SyntaxError(f"Expected '>', but found '{_temp.value if _temp else 'None'}'")

        tokens: List[str] = [self._consume("TEMPLATE_END").value]
        depth: int = 1
        while depth > 0:
            token: Token = self._consume()
            tokens.append(token.value)
            if token.type_ == "TEMPLATE_END":
                depth += 1
            elif token.type_ == "TEMPLATE_START":
                depth -= 1

        return ''.join(tokens[::-1])

    def _parse_scopes(self) -> Optional[List[Scope]]:
        """
        Parses namespace or class scopes, if present.

        Returns:
            Optional[List[Scope]]: A list of Scope objects, or None if no scopes found.
        """
        if not self._match("SCOPE"):
            return None

        scopes: List[Scope] = []

        while not self._match("WHITESPACE") and self._peek():
            self._consume("SCOPE")
            template: Optional[str] = self._parse_nested_templates() if self._match("TEMPLATE_END") else None
            token: Token = self._consume("MEMBER")

            scopes.append(Scope(token.value, template))

        return scopes[::-1]

    def _parse_return_type(self) -> Optional[str]:
        """
        Parses any tokens remaining at the start of the string as a return type.

        Returns:
            Optional[str]: The return type as a string, or None if not found.
        """
        if self._match("WHITESPACE"):
            self._consume("WHITESPACE")

        if not self._peek():
            return None

        return_type: List[str] = []
        while self._peek():
            token = self._consume()
            return_type.append(token.value)

        return ''.join(return_type[::-1])
