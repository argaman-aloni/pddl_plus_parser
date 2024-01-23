"""Module to perform numeric symbolic operations on strings representing numeric expressions."""

import re
from typing import Dict

from sympy import symbols, simplify, Expr, Add, Mul, Pow, Symbol, Float
from sympy.core.numbers import Zero
from sympy.parsing.sympy_parser import parse_expr

SYMPY_OP_TO_PDDL_OP = {
    Add: "+",
    Mul: "*",
    Pow: "^",
    Float: "",
    Symbol: "",
    Zero: "0",
}


def extract_atom(expression: Expr, symbols_map: Dict[Symbol, str]) -> str:
    """Extracts an atom from a symbolic expression.

    :param expression: The atomic symbolic expression to extract.
    :param symbols_map: the map between the symbolic expression and the PDDL expression.
    :return: the PDDL expression.
    """
    if expression.func == Float:
        return f"{expression:.2f}"

    if expression.func == Zero:
        return "0"

    elif expression.func == Symbol:
        return f"{symbols_map[expression]}"


def _convert_internal_expression_to_pddl(expression: Expr, operator: str, symbols_map: dict) -> str:
    """Converts the internal expression to a PDDL format.

    :param expression: the expression to convert.
    :param operator: the numeric operator of the current sympy expression.
    :param symbols_map: the map between the symbolic expression and the PDDL expression.
    :return: the string representing the PDDL expression.
    """
    if expression.is_Atom:
        return extract_atom(expression, symbols_map)

    # the expression is a binary expression with multiple arguments
    components = [_convert_internal_expression_to_pddl(
        expression.args[i], SYMPY_OP_TO_PDDL_OP[expression.args[i].func], symbols_map) for i in
        range(len(expression.args))]

    nested_expression = ""
    for component in reversed(components):
        if nested_expression:
            nested_expression = f"({operator} {component} {nested_expression})"
        else:
            nested_expression = component

    return nested_expression


def convert_expr_to_pddl(expr: Expr, symbolic_vars: Dict[str, Symbol]) -> str:
    """Converts a symbolic expression to a PDDL expression.

    :param expr: the symbolic expression to convert.
    :param symbolic_vars: the map between the symbolic expression and the PDDL expression.
    :return: the PDDL expression.
    """
    initial_operator = SYMPY_OP_TO_PDDL_OP[expr.func]
    return _convert_internal_expression_to_pddl(
        expr, initial_operator, {val: key for key, val in symbolic_vars.items()}
    )


def simplify_complex_numeric_expression(complex_numeric_expression: str) -> str:
    """Simplifies a complex numeric expression.

    Note: The expression should not be in PDD: format but in regular mathematical format.

    :param complex_numeric_expression: the expression to simplify.
    :return: the simplified expression in PDDL format.
    """
    # Extract the left part of the inequality
    pddl_variables = set(re.findall(r"(\([\w-]+\s[?\w\-\s]*\))", complex_numeric_expression))
    if len(pddl_variables) == 0:
        return complex_numeric_expression  # Return unchanged if no variables are found

    # the code works on the left side of the numerical inequality
    symbolic_vars = {var: symbols(re.sub(r"[\(\-\)\s\?]", "", var)) for var in pddl_variables}
    # Replace PDDL variables in the left part with symbolic variables
    left_part_str = complex_numeric_expression
    for var, sym in symbolic_vars.items():
        left_part_str = left_part_str.replace(var, str(sym))

    # Convert the modified left part back to a symbolic expression
    left_part_expr = parse_expr(left_part_str)

    # Simplify the left part
    simplified_left_part = simplify(left_part_expr)
    return convert_expr_to_pddl(simplified_left_part, symbolic_vars)
