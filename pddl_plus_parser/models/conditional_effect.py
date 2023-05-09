"""Module to handle the functionality of conditional effects."""
from typing import Union, Set

from .pddl_precondition import CompoundPrecondition
from .pddl_type import PDDLType
from .pddl_predicate import Predicate, GroundedPredicate
from .numerical_expression import NumericalExpressionTree


class ConditionalEffect:
    """Class representing a conditional effect in a PDDL+ action."""

    antecedents: CompoundPrecondition
    discrete_effects: Set[Union[Predicate, GroundedPredicate]]
    numeric_effects: Set[NumericalExpressionTree]

    def __init__(self):
        self.antecedents = CompoundPrecondition()
        self.discrete_effects = set()
        self.numeric_effects = set()

    def __str__(self):
        discrete_effect = "\n\t".join([effect.untyped_representation for effect in self.discrete_effects])
        numeric_effect = "\n\t".join([effect.to_pddl() for effect in self.numeric_effects])

        return f"(when {str(self.antecedents)} " \
               f"(and {discrete_effect}{numeric_effect}))"


class UniversalEffect:
    """Class representing a universal quantifier in a PDDL+ action."""

    quantified_parameter: str
    quantified_type: PDDLType
    conditional_effects: Set[ConditionalEffect]

    def __init__(self, quantified_parameter: str, quantified_type: PDDLType):
        self.quantified_parameter = quantified_parameter
        self.quantified_type = quantified_type
        self.conditional_effects = set()

    def __str__(self):
        if len(self.conditional_effects) == 0:
            return ""

        combined_universal_effect = ""
        for conditional_effect in self.conditional_effects:
            combined_universal_effect += f"(forall ({self.quantified_parameter} - {self.quantified_type.name})" \
                                         f"\n\t\t{str(conditional_effect)})\n\t"
        return combined_universal_effect
