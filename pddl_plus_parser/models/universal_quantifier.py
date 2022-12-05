"""Model representing a universal quantifier in a PDDL+ action."""
from typing import Set

from pddl_plus_parser.models.pddl_predicate import Predicate
from pddl_plus_parser.models.pddl_type import PDDLType
from pddl_plus_parser.models.conditional_effect import ConditionalEffect


class UniversalQuantifiedPrecondition:
    """Class representing a universally quantified precondition."""

    quantified_parameter: str
    quantified_type: PDDLType
    positive_conditions: Set[Predicate]
    negative_conditions: Set[Predicate]

    def __init__(self, quantified_parameter: str, quantified_type: PDDLType, positive_conditions: Set[Predicate],
                 negative_conditions: Set[Predicate]):
        self.quantified_parameter = quantified_parameter
        self.quantified_type = quantified_type
        self.positive_conditions = positive_conditions
        self.negative_conditions = negative_conditions

    def __str__(self):
        positive_conditionals = "\n\t".join([cond.untyped_representation for cond in self.positive_conditions])
        negative_conditionals = "\n\t".join([f"(not {negative_cond.untyped_representation})" for
                                             negative_cond in self.negative_conditions])
        return f"(forall ({self.quantified_parameter} - {self.quantified_type.name})" \
               f"\n\t{positive_conditionals}\n\t{negative_conditionals})"


class UniversalQuantifiedEffect:
    """Class representing a universal quantifier in a PDDL+ action."""

    quantified_parameter: str
    quantified_type: PDDLType
    conditional_effect: ConditionalEffect

    def __init__(self, quantified_parameter: str, quantified_type: PDDLType, conditional_effect: ConditionalEffect):
        self.quantified_parameter = quantified_parameter
        self.quantified_type = quantified_type
        self.conditional_effect = conditional_effect

    def __str__(self):
        return f"(forall ({self.quantified_parameter} - {self.quantified_type.name})" \
               f"\n\t\t{str(self.conditional_effect)})"
