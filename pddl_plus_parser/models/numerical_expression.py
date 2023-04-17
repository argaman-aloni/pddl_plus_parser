"""Class that represents a numerical expression that can be evaluated."""
from typing import List, Union, Dict, Optional

from anytree import AnyNode, RenderTree

from .pddl_function import PDDLFunction

LEGAL_NUMERICAL_EXPRESSIONS = ["=", "!=", "<=", ">=", ">", "<", "+", "-", "/", "*", "increase", "decrease", "assign"]


def construct_expression_tree(expression_ast: List[Union[str, List[str]]],
                              domain_functions: Dict[str, PDDLFunction]) -> AnyNode:
    """Constructs a tree that represents the numerical expression and that is later on able to be evaluated.

    :param expression_ast: the AST representing the numeric expression that is to be parsed.
    :param domain_functions: the functions that are defined in the domain.
    :return: the tree representing the numeric calculation.
    """
    if type(expression_ast) == str:
        if expression_ast in LEGAL_NUMERICAL_EXPRESSIONS:
            raise SyntaxError("Leaf node cannot be a numerical operator!")

        ast_node_item: str = expression_ast
        try:
            return AnyNode(id=f"{float(ast_node_item)}", value=float(ast_node_item))

        except ValueError:
            raise SyntaxError("Leaf node with bad string was encountered!")

    # This means that we have a list as a leaf --> a function that we need to create.
    elif all([type(item) == str for item in expression_ast]):
        function_name = expression_ast[0]
        extracted_function = domain_functions[function_name]
        if len(expression_ast) == 1:
            return AnyNode(id=str(extracted_function), value=extracted_function)

        new_function = PDDLFunction(name=function_name, signature={
            param_name: param_type for param_name, param_type in
            zip(expression_ast[1:], extracted_function.signature.values())
        })
        return AnyNode(id=str(new_function), value=new_function)

    node = AnyNode(id=expression_ast[0], value=expression_ast[0], children=[
        construct_expression_tree(expression_ast[1], domain_functions),
        construct_expression_tree(expression_ast[2], domain_functions)
    ])
    return node


def increase(value_to_increase: PDDLFunction, increase_by: float) -> None:
    """Increase the value of the first numerical fluent by the value of the other.

    :param value_to_increase: the parameter that is to be increased
    :param increase_by: the value to increase the parameter by.
    """
    previous_value = value_to_increase.value
    value_to_increase.set_value(previous_value + increase_by)


def decrease(value_to_decrease: PDDLFunction, decrease_by: float) -> None:
    """Decrease the value of the first numerical fluent by the value of the other.

    :param value_to_decrease: the parameter that is to be decreased
    :param decrease_by: the value to decrease the parameter by.
    """
    previous_value = value_to_decrease.value
    value_to_decrease.set_value(previous_value - decrease_by)


def assign(assigned_variable: PDDLFunction, value_to_assign: float) -> None:
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

ASSIGNMENT_EXPRESSIONS = {
    "increase": increase,
    "decrease": decrease,
    "assign": assign
}

NUMERICAL_BINARY_OPERATORS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
    "*": lambda x, y: x * y,
}


def calculate(expression_node: AnyNode) -> float:
    """Calculates the numerical value of an expression tree.

    :param expression_node: the node that is currently being observed.
    :return: the value that was calculated.
    """
    if len(expression_node.children) == 0:
        if isinstance(expression_node.value, PDDLFunction):
            node_function: PDDLFunction = expression_node.value
            return node_function.value

        return expression_node.value

    numerical_operator = expression_node.value
    left_operand = calculate(expression_node.children[0])
    right_operand = calculate(expression_node.children[1])
    return NUMERICAL_BINARY_OPERATORS[numerical_operator](left_operand, right_operand)


def evaluate_expression(expression_tree: AnyNode) -> Optional[Union[bool, PDDLFunction]]:
    """Evaluates the value of a PDDL expression based on parsing the content of its AST.

    :param expression_tree: the PDDL expression to evaluate.
    :return: bool if the operand is a comparison operand, otherwise assign the calculated value to the function inline.
    """
    if expression_tree.value in ASSIGNMENT_EXPRESSIONS:
        assigned_variable: PDDLFunction = expression_tree.children[0].value
        evaluated_operand = calculate(expression_tree.children[1])
        ASSIGNMENT_EXPRESSIONS[expression_tree.value](assigned_variable, evaluated_operand)
        return assigned_variable

    compared_operator = calculate(expression_tree.children[0])
    evaluated_operand = calculate(expression_tree.children[1])
    return COMPARISON_OPERATORS[expression_tree.value](compared_operator, evaluated_operand)


def set_expression_value(expression_node: AnyNode, state_fluents: Dict[str, PDDLFunction]) -> None:
    """Set the value of the expression according to the fluents present in the state.

    :param expression_node: the node that is currently being observed.
    :param state_fluents: the grounded numeric fluents present in the state.
    """
    if expression_node.is_leaf:
        if not isinstance(expression_node.value, PDDLFunction):
            return

        grounded_fluent: PDDLFunction = expression_node.value
        try:
            grounded_fluent.set_value(state_fluents[grounded_fluent.untyped_representation].value)

        except KeyError:
            grounded_fluent.set_value(0.0)

        return

    set_expression_value(expression_node.children[0], state_fluents)
    set_expression_value(expression_node.children[1], state_fluents)


class NumericalExpressionTree:
    root: AnyNode

    def __init__(self, expression_tree: AnyNode):
        self.root = expression_tree

    def __str__(self):
        return "\n".join([f"{pre}{node.id}" for pre, _, node in RenderTree(self.root)])

    def _convert_to_pddl(self, node: AnyNode) -> str:
        """Recursive method that converts the expression tree to a PDDL string.

        :param node: the node that the recursion is currently working on.
        :return: the PDDL string of the expression.
        """
        if node.is_leaf:
            if isinstance(node.value, PDDLFunction):
                function: PDDLFunction = node.value
                return function.untyped_representation

            return node.value

        left_operand = self._convert_to_pddl(node.children[0])
        right_operand = self._convert_to_pddl(node.children[1])
        return f"({node.value} {left_operand} {right_operand})"

    def to_pddl(self) -> str:
        return self._convert_to_pddl(self.root)
