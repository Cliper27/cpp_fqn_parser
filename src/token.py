from dataclasses import dataclass


@dataclass
class Token:
    type_: str
    value: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Token) and self.type_ == other.type_ and self.value == other.value
