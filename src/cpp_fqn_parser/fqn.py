from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from .scope import Scope
from .utils import to_dict


@dataclass
class FQN:
    """
    Represents a fully qualified name (FQN) of a function, method, or symbol.

    Attributes:
        name (str): The simple (unqualified) name.
        full_name (str): The fully qualified name (e.g., including namespaces or modules).
        return_type (Optional[str]): The return type of the symbol, if known.
        args (Optional[List[str]]): The list of argument types or names.
        scopes (Optional[List[Scope]]): The lexical or semantic scopes the symbol belongs to.
        template (Optional[str]): Template/generic type information, if applicable.
        constant (bool): Whether the symbol represents a constant value.
        volatile (bool): Whether the symbol is considered volatile (e.g., changes frequently or is side-effect-prone).
    """
    name: str
    full_name: str
    return_type: Optional[str] = None
    args: Optional[List[str]] = None
    scopes: Optional[List[Scope]] = None
    template: Optional[str] = None
    constant: bool = False
    volatile: bool = False

    def __eq__(self, other: object) -> bool:
        """
        Compare this FQN instance with another for structural equality.

        Args:
            other (object): Another object to compare with.

        Returns:
            bool: True if `other` is an FQN with equal attributes, False otherwise.
        """
        return (isinstance(other, FQN) and
                self.name == other.name and
                self.full_name == other.full_name and
                self.return_type == other.return_type and
                self.args == other.args and
                self.scopes == other.scopes and
                self.template == other.template and
                self.constant == other.constant and
                self.volatile == other.volatile)

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FQN':
        attrs = ["name", "full_name", "return_type", "args", "scopes", "template", "constant", "volatile"]
        for attr in attrs:
            if attr not in data:
                raise KeyError(f"Missing key '{attr}'")

        return FQN(name=data["name"],
                   full_name=data["full_name"],
                   return_type=data["return_type"],
                   args=data["args"],
                   scopes=[Scope.from_dict(scope) for scope in data["scopes"]],
                   template=data["template"],
                   constant=data["constant"],
                   volatile=data["volatile"])
