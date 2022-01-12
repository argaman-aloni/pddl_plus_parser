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
    constants: List[PDDLConstant]
    predicates: Dict[str, Predicate]
    functions: Dict[str, PDDLFunction]
    actions: Dict[str, Action]
    # processes: Dict[str, Action] - TBD
    # events: Dict[str, Action] - TBD
