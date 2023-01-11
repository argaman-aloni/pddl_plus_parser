"""Module describing disjunctive preconditions."""
from typing import Set, Union, List

from pddl_plus_parser.models import Predicate, NumericalExpressionTree, GroundedPredicate


class DisjunctivePrecondition:
    """Class representing a disjunctive precondition."""

    conjunctions: List[List[Union[Predicate, GroundedPredicate, NumericalExpressionTree, "DisjunctivePrecondition"]]]

    def __init__(self):
        self.conjunctions = []

    @staticmethod
    def _construct_items_conjunction(items: List[Union[Predicate, NumericalExpressionTree]]) -> str:
        """Constructs the string representation of one side of the disjunctive precondition.

        :param items: the side to construct the string representation for.
        :return: the string representation of the side.
        """
        side_str = " "
        if len(items) == 1:
            return items[0].untyped_representation if isinstance(items[0], (Predicate, GroundedPredicate)) \
                else items[0].to_pddl()

        for item in items:
            if isinstance(item, (Predicate, GroundedPredicate)):
                side_str += f" {item.untyped_representation}"

            elif isinstance(item, NumericalExpressionTree):
                side_str += f" {item.to_pddl()}"

            elif isinstance(item, DisjunctivePrecondition):
                side_str += f" {item.__str__()}"

        return f"(and {side_str})"

    def __str__(self):
        """Returns the string representation of the disjunctive precondition."""
        disjunction_components = []
        for conjunction in self.conjunctions:
            conjunction_items = []
            if len(conjunction) == 1:
                conjunction_item = conjunction[0].untyped_representation if isinstance(conjunction[0],
                                                                                       (Predicate, GroundedPredicate)) \
                    else conjunction[0].to_pddl()
                disjunction_components.append(conjunction_item)

            else:
                disjunction_components.append(f" (and {self._construct_items_conjunction(conjunction)})")

        return f"(or {' '.join(disjunction_components)})"
