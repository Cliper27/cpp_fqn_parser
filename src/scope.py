from dataclasses import dataclass
from typing import Optional


@dataclass
class Scope:
    name: str
    template: Optional[str] = None
