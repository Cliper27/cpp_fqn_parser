from dataclasses import dataclass
from typing import Optional


@dataclass
class Scope:
    name: str
    template: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Scope) and self.name == other.name and self.template == other.template
