"""Module representing a PDDL+ effect."""

from typing import Union, Set

from pddl_plus_parser.models import Predicate, GroundedPredicate, NumericalExpressionTree


class Effect:
    """Class representing a PDDL+ effect."""

    discrete_effects: Set[Union[Predicate, GroundedPredicate]]
    numeric_effects: Set[NumericalExpressionTree]

    def __init__(self):
        self.discrete_effects = set()
        self.numeric_effects = set()

    def __str__(self):
        discrete_effect = "\n\t".join([effect.untyped_representation for effect in self.discrete_effects])
        numeric_effect = "\n\t".join([effect.to_pddl() for effect in self.numeric_effects])

        return f"(and {discrete_effect}{numeric_effect})"

    def add_discrete_effect(self, effect: Union[Predicate, GroundedPredicate]) -> None:
        """Add a discrete effect to the effect.

        :param effect: the effect to add
        """
        self.discrete_effects.add(effect)

    def add_numeric_effect(self, effect: NumericalExpressionTree) -> None:
        """Add a numeric effect to the effect.

        :param effect: the effect to add
        """
        self.numeric_effects.add(effect)