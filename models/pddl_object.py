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


PDDLConstant = PDDLObject
