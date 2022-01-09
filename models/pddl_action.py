"""Module that represents a PDDL+ action."""
from typing import Set, Callable, Union

from models import SignatureType, Predicate, PDDLFunction

COMPARISON_OPERATORS = {
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
}


class NumericPrecondition:
    """Class that stores a numeric precondition function"""

    op: Callable  # This needs to be a mathematical operator.
    function: PDDLFunction
    precondition_value: Union[float, PDDLFunction]

    def __init__(self, op: str, function: PDDLFunction, precondition_value: Union[float, PDDLFunction]):
        self.op = COMPARISON_OPERATORS[op]
        self.function = function
        self.precondition_value = precondition_value

    def holds(self):
        if type(self.precondition_value) == PDDLFunction:
            return self.op(self.function.value, self.precondition_value.value)

        return self.op(self.function.value, self.precondition_value)


class Action:
    """Class representing an instant action in a PDDL+ problems."""

    name: str
    signature: SignatureType
    positive_preconditions: Set[Predicate]
    negative_preconditions: Set[Predicate]
    numeric_preconditions: Set[NumericPrecondition]
    add_effects: Set[Predicate]
    delete_effects: Set[Predicate]
    # numeric_effects: TBD
