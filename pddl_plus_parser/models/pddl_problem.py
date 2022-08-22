"""Module to represent PDDL problems and their data."""
from collections import defaultdict
from typing import List, Dict, Set

from .numerical_expression import NumericalExpressionTree
from .pddl_domain import Domain
from .pddl_function import PDDLFunction
from .pddl_object import PDDLObject
from .pddl_predicate import GroundedPredicate

METRICS = {
    "maximize": max,
    "minimize": min
}


class Problem:
    """Class representing a single PDDL problem."""

    domain: Domain
    name: str
    objects: Dict[str, PDDLObject]
    # Maps between a lifted predicate definition to all of its problem groundings
    initial_state_predicates: Dict[str, Set[GroundedPredicate]]
    # Map between the grounded numeric fluent string to the actual function.
    initial_state_fluents: Dict[str, PDDLFunction]
    # Since we don't need to optimize the search on the goal state, the goal state will remain as list.
    goal_state_predicates: List[GroundedPredicate]
    goal_state_fluents: Set[NumericalExpressionTree]
    metric: Dict[str, NumericalExpressionTree]

    def __init__(self, domain: Domain):
        self.name = ""
        self.domain = domain
        self.objects = {}
        self.initial_state_predicates = defaultdict(set)
        self.initial_state_fluents = {}
        self.goal_state_predicates = []
        self.goal_state_fluents = set()
        self.metric = {}

    def __str__(self):
        grounded_predicates = []
        for p in self.initial_state_predicates.values():
            grounded_predicates.extend(p)

        return f"<Problem - {self.name} of domain - {self.domain.name}.\n" \
               f"Initial state predicates - {[str(p) for p in grounded_predicates]}\n" \
               f"Initial state numeric fluents - {[f for f in self.initial_state_fluents]}\n" \
               f"Goal state - {[str(p) for p in self.goal_state_predicates]}" \
               ">"
