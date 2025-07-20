from typing import Dict, Any, List
from dataclasses import dataclass

from .utils import to_dict, check_keys


@dataclass
class Token:
    """
    Represents a lexical token with a type and value.

    Attributes:
        type_ (str): The type/category of the token (e.g., 'MEMBER', 'SCOPE').
        value (str): The string value of the token.
    """
    type_: str
    value: str

    def __eq__(self, other: object) -> bool:
        """
        Compare this token to another for equality.

        Args:
            other (object): Another object to compare with.

        Returns:
            bool: True if `other` is a Token with the same type and value, False otherwise.
        """
        return isinstance(other, Token) and self.type_ == other.type_ and self.value == other.value

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Token':
        attrs: List[str] = ["type_", "value"]
        check_keys(attrs, data)
        return Token(type_=data["type_"],
                     value=data["value"])
