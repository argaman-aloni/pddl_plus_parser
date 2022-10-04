"""Module to handle the functionality of conditional effects."""
from typing import Union, Set

from .pddl_predicate import Predicate, GroundedPredicate
from .numerical_expression import NumericalExpressionTree


class ConditionalEffect:
    """Class representing a conditional effect in a PDDL+ action."""

    positive_conditions: Set[Union[Predicate, GroundedPredicate]]
    negative_conditions: Set[Union[Predicate, GroundedPredicate]]
    numeric_conditions: Set[NumericalExpressionTree]
    add_effects: Set[Union[Predicate, GroundedPredicate]]
    delete_effects: Set[Union[Predicate, GroundedPredicate]]
    numeric_effects: Set[NumericalExpressionTree]

    def __init__(self):
        self.positive_conditions = set()
        self.negative_conditions = set()
        self.numeric_conditions = set()
        self.add_effects = set()
        self.delete_effects = set()
        self.numeric_effects = set()

    def __str__(self):
        positive_conditionals = "\n\t".join([cond.untyped_representation for cond in self.positive_conditions])
        negative_conditionals = "\n\t".join(
            [f"(not {negative_cond.untyped_representation})" for negative_cond in self.negative_conditions])
        numeric_conditionals = "\n\t".join([cond.to_pddl() for cond in self.numeric_conditions])
        add_effect = "\n\t".join([effect.untyped_representation for effect in self.add_effects])
        delete_effect = "\n\t".join(
            [f"(not {negative_effect.untyped_representation})" for negative_effect in self.delete_effects])
        discrete_effect = add_effect + delete_effect
        numeric_effect = "\n\t".join([effect.to_pddl() for effect in self.numeric_effects])

        return f"(when (and {positive_conditionals}{negative_conditionals}{numeric_conditionals}) " \
               f"(and {discrete_effect}{numeric_effect}))"
