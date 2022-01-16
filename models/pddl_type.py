"""Module that contains the definition of PDDL+ types"""
from typing import Optional


class PDDLType:
    name: str
    parent: Optional["PDDLType"]

    def __init__(self, name: str, parent: Optional["PDDLType"] = None):
        self.name = name.lower()
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.parent is not None:
            return f"type: {self.name} descendant of {str(self.parent)}"

        return f"type: {self.name}"

    def __eq__(self, other: "PDDLType"):
        return self.name == other.name

    def is_sub_type(self, other_type: "PDDLType") -> bool:
        """Checks if a type a subtype of the other.

        :param other_type: the type that is checked to se if the first is subtype of.
        :return: whether or not the first is a subtype of the other.
        """
        compared_type = self
        while compared_type.parent is not None:
            if compared_type.name == other_type.name:
                return True

            compared_type = compared_type.parent

        return False
