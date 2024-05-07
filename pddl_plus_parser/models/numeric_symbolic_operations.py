"""Module to perform numeric symbolic operations on strings representing numeric expressions."""

import re
from typing import Dict, Optional

from sympy import symbols, simplify, Expr, Add, Mul, Pow, Symbol, Float
from sympy.core.numbers import Zero, NegativeOne, One, Integer
from sympy.parsing.sympy_parser import parse_expr

SYMPY_OP_TO_PDDL_OP = {
    Add: "+",
    Mul: "*",
    Pow: "^",
    Float: "",
    Integer: "",
    Symbol: "",
    Zero: "0",
    NegativeOne: "-1",
    One: "1",
}


def extract_atom(expression: Expr, symbols_map: Dict[Symbol, str]) -> Optional[str]:
    """Extracts an atom from a symbolic expression.

    :param expression: The atomic symbolic expression to extract.
    :param symbols_map: the map between the symbolic expression and the PDDL expression.
    :return: the PDDL expression.
    """
    if expression.func == Float:
        formatted_expression = format(expression, ".4f")
        return formatted_expression if float(formatted_expression) != 0 else None

    if expression.func == Integer:
        return f"{expression}"

    if expression.func == Zero:
        return "0"

    if expression.func == One:
        return "1"

    if expression.func == NegativeOne:
        return "-1"

    if expression.func == Symbol:
        return f"{symbols_map[expression]}"

    raise ValueError(f"Unsupported atomic expression: {expression}")


def _recursive_pow_expression_to_pddl(expression: Pow, symbols_map: dict) -> str:
    """Converts a recursive expression to a PDDL format.

    :param expression: the expression to convert.
    :return: the string representing the PDDL expression.
    """
    exponent = expression.exp
    compiled_expression = f"{symbols_map[expression.base]}"
    if exponent == -1:
        return f"(/ 1 {compiled_expression})"

    for _ in range(exponent - 1):
        compiled_expression = f"(* {compiled_expression} {symbols_map[expression.base]})"

    return compiled_expression


def _convert_internal_expression_to_pddl(expression: Expr, operator: str, symbols_map: dict) -> str:
    """Converts the internal expression to a PDDL format.

    :param expression: the expression to convert.
    :param operator: the numeric operator of the current sympy expression.
    :param symbols_map: the map between the symbolic expression and the PDDL expression.
    :return: the string representing the PDDL expression.
    """
    if expression.is_Atom:
        return extract_atom(expression, symbols_map)

    if isinstance(expression, Pow) and expression.exp == -1:
        return f"(/ 1 {_convert_internal_expression_to_pddl(expression.base, SYMPY_OP_TO_PDDL_OP[expression.base.func], symbols_map)})"

    if isinstance(expression, Pow) and expression.exp > 1:
        return _recursive_pow_expression_to_pddl(expression, symbols_map)

    # the expression is a binary expression with multiple arguments
    components = []
    for i in range(len(expression.args)):
        comp = _convert_internal_expression_to_pddl(
            expression.args[i], SYMPY_OP_TO_PDDL_OP[expression.args[i].func], symbols_map)
        if comp:
            components.append(comp)

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
