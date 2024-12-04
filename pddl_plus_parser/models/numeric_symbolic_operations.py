"""Module to perform numeric symbolic operations on strings representing numeric expressions."""
import os
import re
from typing import Dict, Optional, List, Tuple

from sympy import Eq, sympify, expand
from sympy import symbols, simplify, Expr, Add, Mul, Pow, Symbol, Float
from sympy.core.numbers import Zero, NegativeOne, One, Integer
from sympy.logic.boolalg import BooleanTrue
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

DEFAULT_DECIMAL_DIGITS = os.environ.get("NUMERIC_PRECISION", 4)


def is_number_string(s):
    pattern = re.compile(r'^-?\d+(\.\d+)?$')
    return bool(pattern.match(s))


def extract_atom(expression: Expr, symbols_map: Dict[Symbol, str], decimal_digits: int = DEFAULT_DECIMAL_DIGITS,
                 should_remove_trailing_zeros: bool = True) -> \
        Optional[str]:
    """Extracts an atom from a symbolic expression.

    :param expression: The atomic symbolic expression to extract.
    :param symbols_map: the map between the symbolic expression and the PDDL expression.
    :param decimal_digits: the number of decimal digits to keep.
    :param should_remove_trailing_zeros: whether to remove trailing zeros or not.
    :return: the PDDL expression.
    """
    if expression.func == Float:
        formatted_expression = format(expression, f".{decimal_digits}f") if not \
            round(float(expression), decimal_digits).is_integer() else f"{int(expression)}"
        if should_remove_trailing_zeros:
            return formatted_expression if float(formatted_expression) != 0 else None

        return formatted_expression

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


def _convert_internal_expression_to_pddl(expression: Expr, operator: str, symbols_map: dict,
                                         decimal_digits: int = DEFAULT_DECIMAL_DIGITS,
                                         should_remove_trailing_zeros: bool = True) -> str:
    """Converts the internal expression to a PDDL format.

    :param expression: the expression to convert.
    :param operator: the numeric operator of the current sympy expression.
    :param symbols_map: the map between the symbolic expression and the PDDL expression.
    :param decimal_digits: the number of decimal digits to keep.
    :return: the string representing the PDDL expression.
    """
    if expression.is_Atom:
        return extract_atom(expression, symbols_map, decimal_digits, should_remove_trailing_zeros)

    if isinstance(expression, Pow) and expression.exp == -1:
        return f"(/ 1 {_convert_internal_expression_to_pddl(expression.base, SYMPY_OP_TO_PDDL_OP[expression.base.func], symbols_map, decimal_digits, should_remove_trailing_zeros)})"

    if isinstance(expression, Pow) and expression.exp > 1:
        return _recursive_pow_expression_to_pddl(expression, symbols_map)

    # the expression is a binary expression with multiple arguments
    components = []
    for i in range(len(expression.args)):
        comp = _convert_internal_expression_to_pddl(
            expression.args[i], SYMPY_OP_TO_PDDL_OP[expression.args[i].func], symbols_map, decimal_digits,
            should_remove_trailing_zeros)
        if comp:
            components.append(comp)

    nested_expression = ""
    for component in reversed(components):
        if nested_expression:
            nested_expression = f"({operator} {component} {nested_expression})" if not is_number_string(
                components[0]) else f"({operator} {nested_expression} {component})"

        else:
            nested_expression = component

    return nested_expression


def convert_expr_to_pddl(expr: Expr, symbolic_vars: Dict[str, Symbol],
                         decimal_digits: int = DEFAULT_DECIMAL_DIGITS,
                         should_remove_trailing_zeros: bool = True) -> str:
    """Converts a symbolic expression to a PDDL expression.

    :param expr: the symbolic expression to convert.
    :param symbolic_vars: the map between the symbolic expression and the PDDL expression.
    :param decimal_digits: the number of decimal digits to keep.
    :param should_remove_trailing_zeros: whether to remove trailing zeros or not.
    :return: the PDDL expression.
    """
    initial_operator = SYMPY_OP_TO_PDDL_OP[expr.func]
    return _convert_internal_expression_to_pddl(
        expr, initial_operator, {val: key for key, val in symbolic_vars.items()}, decimal_digits=decimal_digits,
        should_remove_trailing_zeros=should_remove_trailing_zeros
    )


def transform_expression(expression: str, symbols_to_use: Optional[Dict[str, Symbol]] = None) -> Tuple[
    str, Dict[str, Symbol]]:
    """

    :param expression:
    :param symbols_to_use:
    :return:
    """
    pddl_variables = set(re.findall(r"(\([\w-]+\s[?\w\-\s]*\))", expression))
    if len(pddl_variables) == 0:
        return expression, symbols_to_use

    # Extract the left part of the inequality
    symbolic_vars = {**symbols_to_use} if symbols_to_use else {}
    for var in pddl_variables:
        if var not in symbolic_vars:
            symbolic_vars[var] = symbols(re.sub(r"[\(\-\)\s\?]", "", var))

    formatted_expression = expression
    for var, sym in symbolic_vars.items():
        formatted_expression = formatted_expression.replace(var, str(sym))

    return formatted_expression, symbolic_vars


def simplify_complex_numeric_expression(complex_numeric_expression: str,
                                        decimal_digits: int = DEFAULT_DECIMAL_DIGITS) -> str:
    """Simplifies a complex numeric expression.

    Note: The expression should not be in PDD: format but in regular mathematical format.

    :param complex_numeric_expression: the expression to simplify.
    :param decimal_digits: the number of decimal digits to keep.
    :return: the simplified expression in PDDL format.
    """
    left_part_str, symbolic_vars = transform_expression(complex_numeric_expression)
    left_part_expr = parse_expr(left_part_str)
    simplified_expression = simplify(left_part_expr)
    return convert_expr_to_pddl(simplified_expression, symbolic_vars, decimal_digits=decimal_digits)


def simplify_equality(equation: str, decimal_digits=DEFAULT_DECIMAL_DIGITS) -> Optional[str]:
    """

    :param equation:
    :param decimal_digits:
    :return:
    """
    left_expr, right_expr = equation.split('=')
    transformed_left_expr, symbolic_vars = transform_expression(left_expr)
    transformed_right_expr, symbolic_vars = transform_expression(right_expr, symbolic_vars)
    transformed_left_expr = parse_expr(transformed_left_expr, evaluate=False)
    transformed_right_expr = parse_expr(transformed_right_expr, evaluate=False)
    equation = Eq(transformed_left_expr, transformed_right_expr)
    simplified_equation = simplify(equation)

    if isinstance(simplified_equation, BooleanTrue):
        return None

    pddl_left_side = convert_expr_to_pddl(simplified_equation.lhs, symbolic_vars, decimal_digits=decimal_digits)
    pddl_right_side = convert_expr_to_pddl(simplified_equation.rhs, symbolic_vars, decimal_digits=decimal_digits,
                                           should_remove_trailing_zeros=False)

    return f"(= {pddl_left_side} {pddl_right_side})"


def simplify_inequality(complex_numeric_expression: str, inequality_operator: str, assumptions: List[str] = [],
                        decimal_digits=DEFAULT_DECIMAL_DIGITS) -> Optional[str]:
    """Simplifies a complex numeric inequality by performing the following steps:

    1. if there are assumptions, substitute them into the inequality
    2. expand the brackets in the expression

    :param complex_numeric_expression: the expression to simplify.
    :param inequality_operator: the operator of the inequality.
    :param assumptions: the assumptions to substitute into the inequality.
    :param decimal_digits: the number of decimal digits to keep.
    :return: the simplified expression in PDDL format.
    """
    left_side_expression, right_side_expression = complex_numeric_expression[1:-1].split(inequality_operator)
    transformed_left_str, symbolic_vars = transform_expression(left_side_expression)
    transformed_right_str, symbolic_vars = transform_expression(right_side_expression, symbolic_vars)
    left_expr = parse_expr(transformed_left_str, evaluate=False)
    right_expr = parse_expr(transformed_right_str, evaluate=False)

    for assumption_str in assumptions:
        # Parse the strings as sympy expressions
        assumption_expression, symbolic_vars = transform_expression(assumption_str, symbolic_vars)
        lhs, rhs = assumption_expression.split('=')
        lhs = simplify(sympify(lhs))
        rhs = simplify(sympify(rhs))
        assumption = simplify(Eq(lhs, rhs))
        left_expr = left_expr.subs(assumption.lhs, assumption.rhs)
        right_expr = right_expr.subs(assumption.lhs, assumption.rhs)

    pddl_left_side = convert_expr_to_pddl(expand(left_expr), symbolic_vars, decimal_digits=decimal_digits)
    pddl_right_side = convert_expr_to_pddl(expand(right_expr), symbolic_vars, decimal_digits=decimal_digits,
                                           should_remove_trailing_zeros=False)

    return f"({inequality_operator} {pddl_left_side} {pddl_right_side})"
