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
