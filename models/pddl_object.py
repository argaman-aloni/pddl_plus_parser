"""Module representing the objects and constants of PDDL files."""
from models import PDDLType


class PDDLObject:
    name: str
    type: PDDLType

    def __init__(self, name: str, type: PDDLType):
        self.name = name
        self.type = type


class PDDLConstant:
    name: str
    type: PDDLType

    def __init__(self, name: str, type: PDDLType):
        self.name = name
        self.type = type
