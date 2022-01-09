"""Module that represents a PDDL+ domain"""
from typing import List, Dict

from models import PDDLType, PDDLConstant, Predicate, PDDLFunction, Action


class Domain:
    """Class representing the PDDL+ domain object."""

    name: str
    requirements: List[str]
    types: Dict[str, PDDLType]
    constants: List[PDDLConstant]
    predicates: Dict[str, Predicate]
    functions: Dict[str, PDDLFunction]
    actions: Dict[str, Action]
    # processes: Dict[str, Action] TBD
    # events: Dict[str, Action] TBD

