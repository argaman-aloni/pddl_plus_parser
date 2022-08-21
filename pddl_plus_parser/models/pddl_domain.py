"""Module that represents a PDDL+ domain"""
from typing import List, Dict

from .pddl_action import Action
from .pddl_function import PDDLFunction
from .pddl_object import PDDLConstant
from .pddl_predicate import Predicate
from .pddl_type import PDDLType


class Domain:
    """Class representing the PDDL+ domain object."""

    name: str
    requirements: List[str]
    types: Dict[str, PDDLType]
    constants: Dict[str, PDDLConstant]
    predicates: Dict[str, Predicate]
    functions: Dict[str, PDDLFunction]
    actions: Dict[str, Action]

    # processes: Dict[str, Action] - TBD
    # events: Dict[str, Action] - TBD

    def __init__(self):
        self.actions = {}
        self.constants = {}
        self.functions = {}
        self.types = {}
        self.predicates = {}
        self.requirements = []

    def __str__(self):
        return (
                "< Domain definition: %s\n Requirements: %s\n Predicates: %s\n Functions: %s\n Actions: %s\n "
                "Constants: %s >"
                % (
                    self.name,
                    [req for req in self.requirements],
                    [str(p) for p in self.predicates.values()],
                    [str(f) for f in self.functions.values()],
                    [str(a) for a in self.actions],
                    [str(c) for c in self.constants],
                )
        )
