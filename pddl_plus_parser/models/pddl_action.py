"""Module that represents a PDDL+ action."""
from typing import Set, List

from .conditional_effect import ConditionalEffect, UniversalEffect
from .numerical_expression import NumericalExpressionTree
from .pddl_precondition import CompoundPrecondition
from .pddl_predicate import SignatureType, Predicate


class Action:
    """Class representing an instantaneous action in a PDDL+ problems."""

    name: str
    signature: SignatureType
    preconditions: CompoundPrecondition

    discrete_effects: Set[Predicate]
    conditional_effects: Set[ConditionalEffect]
    universal_effects: Set[UniversalEffect]
    numeric_effects: Set[NumericalExpressionTree]

    def __init__(self):
        self.discrete_effects = set()
        self.numeric_effects = set()
        self.conditional_effects = set()
        self.universal_effects = set()

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    @property
    def parameter_names(self) -> List[str]:
        return list(self.signature.keys())
