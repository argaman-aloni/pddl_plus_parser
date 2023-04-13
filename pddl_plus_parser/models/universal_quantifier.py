"""Model representing a universal quantifier in a PDDL+ action."""
from typing import Set

from pddl_plus_parser.models.pddl_predicate import Predicate
from pddl_plus_parser.models.pddl_type import PDDLType
from pddl_plus_parser.models.conditional_effect import ConditionalEffect


class UniversalQuantifiedPrecondition:
    """Class representing a universally quantified precondition."""

    quantified_parameter: str
    quantified_type: PDDLType
    discrete_conditions: Set[Predicate]
    # TODO: Add numeric conditions

    def __init__(self, quantified_parameter: str, quantified_type: PDDLType, conditions: Set[Predicate]):
        self.quantified_parameter = quantified_parameter
        self.quantified_type = quantified_type
        self.discrete_conditions = conditions

    def __str__(self):
        conditions = "\n\t".join([cond.untyped_representation for cond in self.discrete_conditions])
        return f"(forall ({self.quantified_parameter} - {self.quantified_type.name})" \
               f"\n\t{conditions})"


class UniversalQuantifiedEffect:
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

        conditional_effects = "\n\t".join([str(conditional_effect) for conditional_effect in self.conditional_effects])
        return f"(forall ({self.quantified_parameter} - {self.quantified_type.name})" \
               f"\n\t\t{conditional_effects})"
