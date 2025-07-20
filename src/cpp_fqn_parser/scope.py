from dataclasses import dataclass
from typing import Optional, Dict, Any

from .utils import to_dict


@dataclass
class Scope:
    """
    Represents a lexical or semantic scope, such as a namespace, class, or function context.

    Attributes:
        name (str): The name of the scope (e.g., function name, class name, or module).
        template (Optional[str]): Template or generic parameter associated with the scope, if any.
    """
    name: str
    template: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Scope) and self.name == other.name and self.template == other.template

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Scope':
        attrs = ["name", "template"]
        for attr in attrs:
            if attr not in data:
                raise KeyError(f"Missing key '{attr}'")

        return Scope(name=data["name"],
                     template=data["template"])
