"""Module that represents a PDDL+ action."""
from typing import Set, List, Tuple

from .conditional_effect import ConditionalEffect
from .numerical_expression import NumericalExpressionTree
from .pddl_predicate import SignatureType, Predicate


class Action:
    """Class representing an instantaneous action in a PDDL+ problems."""

    name: str
    signature: SignatureType
    positive_preconditions: Set[Predicate]
    negative_preconditions: Set[Predicate]
    numeric_preconditions: Set[NumericalExpressionTree]
    equality_preconditions: Set[Tuple[str, str]]
    inequality_preconditions: Set[Tuple[str, str]]
    add_effects: Set[Predicate]
    delete_effects: Set[Predicate]
    conditional_effects: Set[ConditionalEffect]    # Currently only supporting discrete conditional effects.
    numeric_effects: Set[NumericalExpressionTree]
    # currently only supporting disjunction of numeric preconditions
    disjunctive_numeric_preconditions: List[Set[NumericalExpressionTree]]

    def __init__(self):
        self.positive_preconditions = set()
        self.negative_preconditions = set()
        self.numeric_preconditions = set()
        self.equality_preconditions = set()
        self.inequality_preconditions = set()
        self.add_effects = set()
        self.delete_effects = set()
        self.numeric_effects = set()
        self.disjunctive_numeric_preconditions = []

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    @property
    def parameter_names(self) -> List[str]:
        return list(self.signature.keys())
