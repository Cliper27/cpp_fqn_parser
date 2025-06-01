from dataclasses import dataclass
from typing import Optional, List

from .scope import Scope


@dataclass
class FQN:
    name: str
    full_name: str
    return_type: Optional[str] = None
    args: Optional[List[str]] = None
    scopes: Optional[List[Scope]] = None
    template: Optional[str] = None
    constant: bool = False
    volatile: bool = False

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, FQN) and
                self.name == other.name and
                self.full_name == other.full_name and
                self.return_type == other.return_type and
                self.args == other.args and
                self.scopes == other.scopes and
                self.template == other.template and
                self.constant == other.constant and
                self.volatile == other.volatile)
