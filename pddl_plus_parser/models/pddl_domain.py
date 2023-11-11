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

    def shallow_copy(self) -> "Domain":
        """Creates a shallow copy of the domain without the actions internal structure."""
        new_domain = Domain()
        new_domain.name = self.name
        new_domain.requirements = self.requirements.copy()
        new_domain.types = {k: v.copy() for k, v in self.types.items()}
        new_domain.constants = {k: v.copy() for k, v in self.constants.items()}
        new_domain.predicates = {k: v.copy() for k, v in self.predicates.items()}
        new_domain.functions = {k: v.copy() for k, v in self.functions.items()}
        for action in self.actions.values():
            copied_action = Action()
            copied_action.name = action.name
            copied_action.signature = action.signature.copy()
            new_domain.actions[action.name] = copied_action

        return new_domain
