"""Module that represents a PDDL+ action."""
from typing import Set, Callable, Union, NoReturn, List

from .numerical_expression import NumericalExpressionTree
from .pddl_function import PDDLFunction
from .pddl_predicate import SignatureType, Predicate


def increase(value_to_increase: PDDLFunction, increase_by: float) -> NoReturn:
    """Increase the value of the first numerical fluent by the value of the other.

    :param value_to_increase: the parameter that is to be increased
    :param increase_by: the value to increase the parameter by.
    """
    previous_value = value_to_increase.value
    value_to_increase.set_value(previous_value + increase_by)


def decrease(value_to_decrease: PDDLFunction, decrease_by: float) -> NoReturn:
    """Decrease the value of the first numerical fluent by the value of the other.

    :param value_to_decrease: the parameter that is to be decreased
    :param decrease_by: the value to decrease the parameter by.
    """
    previous_value = value_to_decrease.value
    value_to_decrease.set_value(previous_value - decrease_by)


def assign(assigned_variable: PDDLFunction, value_to_assign: float) -> NoReturn:
    """assigns the value of one numeric variable to another variable.

    :param assigned_variable: the variable that is being assigned a new value.
    :param value_to_assign: the value that is being assigned to the input variable.
    """
    assigned_variable.set_value(value_to_assign)


COMPARISON_OPERATORS = {
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
}

NUMERIC_EXPRESSIONS = {
    "increase": increase,
    "decrease": decrease,
    "assign": assign
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


class NumericEffect:
    """Class that represents the possible numeric effects that an action can have."""

    op: Callable  # The action to be taken on the effected numerical operand (=fluent).
    affected_function: PDDLFunction
    affecting_operand: Union[float, PDDLFunction]

    def __init__(self, op: str, affected_function: PDDLFunction, affecting_operand: Union[float, PDDLFunction]):
        self.op = NUMERIC_EXPRESSIONS[op]
        self.affected_function = affected_function
        self.affecting_operand = affecting_operand

    def apply(self):
        """applies the function on the affected operator."""
        if type(self.affecting_operand) == PDDLFunction:
            return self.op(self.affected_function, self.affecting_operand.value)

        return self.op(self.affected_function, self.affecting_operand)


class Action:
    """Class representing an instantaneous action in a PDDL+ problems."""

    name: str
    signature: SignatureType
    positive_preconditions: Set[Predicate]
    negative_preconditions: Set[Predicate]
    numeric_preconditions: Set[NumericalExpressionTree]
    add_effects: Set[Predicate]
    delete_effects: Set[Predicate]
    numeric_effects: Set[NumericalExpressionTree]

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    @property
    def parameter_names(self) -> List[str]:
        return list(self.signature.keys())
