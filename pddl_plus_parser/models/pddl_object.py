"""Module representing the objects and constants of PDDL files."""

from .pddl_type import PDDLType


class PDDLObject:
    name: str
    type: PDDLType

    def __init__(self, name: str, type: PDDLType):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.name} - {self.type.name}"

    def copy(self) -> "PDDLObject":
        return PDDLObject(self.name, self.type)

    def __eq__(self, other: "PDDLObject") -> bool:
        if self.name == other.name and self.type != other.type:
            raise ValueError(
                f"Trying to compare two objects with the same name but different types: {self} and {other}"
            )

        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


PDDLConstant = PDDLObject
