"""Module to perform numeric symbolic operations on strings representing numeric expressions."""
import os
import re
from typing import Dict, Optional, List, Tuple

from sympy import Le, Ge, Lt, Eq, Gt
from sympy import symbols, simplify, Expr, Add, Mul, Pow, Symbol, Float, expand, collect
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
    :return: the PDDL expression.
    """
    initial_operator = SYMPY_OP_TO_PDDL_OP[expr.func]
    return _convert_internal_expression_to_pddl(
        expr, initial_operator, {val: key for key, val in symbolic_vars.items()}, decimal_digits=decimal_digits,
        should_remove_trailing_zeros=should_remove_trailing_zeros
    )


def simplify_complex_numeric_expression(complex_numeric_expression: str,
                                        decimal_digits: int = DEFAULT_DECIMAL_DIGITS) -> str:
    """Simplifies a complex numeric expression.

    Note: The expression should not be in PDD: format but in regular mathematical format.

    :param complex_numeric_expression: the expression to simplify.
    :param decimal_digits: the number of decimal digits to keep.
    :return: the simplified expression in PDDL format.
    """
    # Extract the function arguments from the expression
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
    return convert_expr_to_pddl(simplified_left_part, symbolic_vars, decimal_digits=decimal_digits)


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


def get_inequality_operator(inequality: Expr) -> str:
    # Identify the type of the inequality
    inequality_type = type(inequality)

    # Map the type to the corresponding string representation
    operator_map = {
        Le: '<=',
        Ge: '>=',
        Lt: '<',
        Gt: '>',
        Eq: '='
    }

    # Extract and return the operator string
    return operator_map.get(inequality_type, "Unknown operator")


def simplify_equality(equation: str, decimal_digits=DEFAULT_DECIMAL_DIGITS) -> Optional[str]:
    """

    :param equation:
    :param decimal_digits:
    :return:
    """
    left_expr, right_expr = equation.split('=')
    transformed_left_expr, symbolic_vars = transform_expression(left_expr)
    transformed_right_expr, symbolic_vars = transform_expression(right_expr, symbolic_vars)
    transformed_left_expr = parse_expr(transformed_left_expr)
    transformed_right_expr = parse_expr(transformed_right_expr)
    equation = Eq(transformed_left_expr, transformed_right_expr)
    simplified_equation = simplify(equation)

    if isinstance(simplified_equation, BooleanTrue):
        return None

    pddl_left_side = convert_expr_to_pddl(simplified_equation.lhs, symbolic_vars, decimal_digits=decimal_digits)
    pddl_right_side = convert_expr_to_pddl(simplified_equation.rhs, symbolic_vars, decimal_digits=decimal_digits,
                                           should_remove_trailing_zeros=False)

    return f"(= {pddl_left_side} {pddl_right_side})"


def simplify_inequality(complex_numeric_expression: str, assumptions: List[str] = [],
                        decimal_digits=DEFAULT_DECIMAL_DIGITS) -> Optional[str]:
    """

    :param complex_numeric_expression:
    :param assumptions:
    :param decimal_digits:
    :return:
    """
    transformed_expression, symbolic_vars = transform_expression(complex_numeric_expression)
    if not symbolic_vars:
        return complex_numeric_expression

    # Convert the modified left part back to a symbolic expression
    sympy_expression = parse_expr(transformed_expression)

    for assumption in assumptions:
        # Assumption string is expected in the form "expr1 = expr2"
        left_expr, right_expr = assumption.split('=')
        transformed_left_expr, symbolic_vars = transform_expression(left_expr, symbolic_vars)
        transformed_right_expr, symbolic_vars = transform_expression(right_expr, symbolic_vars)
        transformed_left_expr = parse_expr(transformed_left_expr)
        transformed_right_expr = parse_expr(transformed_right_expr)
        equation = Eq(transformed_left_expr, transformed_right_expr)
        simplified_equation = simplify(equation)

        # Substitute the assumption into the inequality
        sympy_expression = sympy_expression.subs(simplified_equation.lhs, simplified_equation.rhs)

    # Expand the brackets in the expression
    expanded_expression = expand(sympy_expression)

    # Step 5: Move all constant terms to the right side and simplify
    inequality_op = get_inequality_operator(expanded_expression)
    simplified_expression = simplify(collect(expanded_expression.lhs - expanded_expression.rhs,
                                             expanded_expression.free_symbols) <= 0) if inequality_op == '<=' \
        else simplify(collect(expanded_expression.lhs - expanded_expression.rhs, expanded_expression.free_symbols) >= 0)

    if isinstance(simplified_expression, BooleanTrue):
        return None

    pddl_left_side = convert_expr_to_pddl(simplified_expression.lhs, symbolic_vars, decimal_digits=decimal_digits)
    pddl_right_side = convert_expr_to_pddl(simplified_expression.rhs, symbolic_vars, decimal_digits=decimal_digits,
                                           should_remove_trailing_zeros=False)

    return f"({get_inequality_operator(simplified_expression)} {pddl_left_side} {pddl_right_side})"
