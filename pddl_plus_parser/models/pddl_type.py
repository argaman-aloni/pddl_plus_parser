"""Module that contains the definition of PDDL+ types"""
from typing import Optional, Dict

import networkx as nx


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

    def copy(self) -> "PDDLType":
        return PDDLType(self.name, self.parent)

    @staticmethod
    def is_sub_type_aux(my_type: "PDDLType", other_type: "PDDLType") -> bool:
        """A recursion to validate that the type is a subtype of the other.

        :param my_type: the type that is checked to see if it is a subtype of the other.
        :param other_type: the type that is checked to see if the first is a subtype of.
        :return: whether the first is a subtype of the other.
        """
        if my_type.name == other_type.name:
            return True

        if my_type.parent is None:
            return False

        return PDDLType.is_sub_type_aux(my_type.parent, other_type)

    def is_sub_type(self, other_type: "PDDLType") -> bool:
        """Checks if a type a subtype of the other.

        :param other_type: the type that is checked to se if the first is subtype of.
        :return: whether the first is a subtype of the other.
        """
        return PDDLType.is_sub_type_aux(self, other_type)


ObjectType = PDDLType(name="object", parent=None)


def create_type_hierarchy_graph(types: Dict[str, PDDLType]) -> nx.DiGraph:
    """
    Constructs a NetworkX directed graph representing the type hierarchy.

    :param types: Dictionary mapping type names to PDDLType objects.
    :return: A directed graph where edges point from a type to its parent.
    """
    hierarchy_graph = nx.DiGraph()

    # Add nodes and edges
    for type_name, pddl_type in types.items():
        hierarchy_graph.add_node(type_name)  # Add node for the type
        if pddl_type.parent:
            hierarchy_graph.add_edge(pddl_type.parent.name, type_name)

    return hierarchy_graph
