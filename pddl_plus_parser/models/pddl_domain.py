"""Module that represents a PDDL+ domain"""
from collections import defaultdict
from typing import List, Dict, Set

from .numerical_expression import DEFAULT_DIGITS
from .pddl_action import Action
from .pddl_function import PDDLFunction
from .pddl_object import PDDLConstant
from .pddl_predicate import Predicate
from .pddl_type import PDDLType, ObjectType

DEFAULT_TYPES = {"object": ObjectType}


class Domain:
    """Class representing the PDDL+ domain object."""

    name: str
    requirements: Set[str]
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
        self.types = DEFAULT_TYPES
        self.predicates = {}
        self.requirements = set()

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

    def _types_to_pddl(self) -> str:
        """Converts the types to a PDDL string.

        :return: the PDDL string representing the types.
        """
        parent_child_map = defaultdict(list)
        if set(self.types.keys()) == {"object"}:
            return "object"

        for type_name, type_obj in self.types.items():
            if type_name == "object":
                continue

            parent_child_map[type_obj.parent.name].append(type_name)

        types_strs = []
        for parent_type, children_types in parent_child_map.items():
            types_strs.append(f"\t{' '.join(children_types)} - {parent_type}")

        return "\n".join(types_strs)

    def _constants_to_pddl(self) -> str:
        """Converts the constants to a PDDL string.

        :return: the PDDL string representing the constants.
        """
        same_type_constant = defaultdict(list)
        for const_name, constant in self.constants.items():
            if const_name == "object":
                continue

            same_type_constant[constant.type.name].append(const_name)

        types_strs = []
        for constant_type_name, constant_objects in same_type_constant.items():
            types_strs.append(f"\t{' '.join(constant_objects)} - {constant_type_name}")

        return "\n".join(types_strs)

    def _functions_to_pddl(self) -> str:
        """Converts the functions to PDDL format.

        :return: the PDDL format of the functions.
        """
        return "\n\t".join([str(f) for f in self.functions.values()])

    def to_pddl(self, decimal_digits: int = DEFAULT_DIGITS) -> str:
        """Converts the domain into a PDDL string format.

        :return: the PDDL string representing the domain.
        """
        self.requirements.update({":negative-preconditions", ":equality"})
        predicates = "\n\t".join([str(p) for p in self.predicates.values()])
        predicates_str = (
            f"(:predicates {predicates}\n)\n\n" if len(self.predicates) > 0 else ""
        )
        types_str = (
            f"(:types {self._types_to_pddl()}\n)\n\n" if len(self.types) > 0 else ""
        )
        actions = "\n".join(
            action.to_pddl(decimal_digits=decimal_digits)
            for action in self.actions.values()
        )
        constants = (
            f"(:constants {self._constants_to_pddl()}\n)\n\n"
            if len(self.constants) > 0
            else ""
        )
        functions = (
            f"(:functions {self._functions_to_pddl()}\n)\n\n"
            if len(self.functions) > 0
            else ""
        )
        return (
            f"(define (domain {self.name})\n"
            f"(:requirements {' '.join(self.requirements)})\n"
            f"{types_str}"
            f"{constants}"
            f"{predicates_str}"
            f"{functions}"
            f"{actions}\n)"
        )
