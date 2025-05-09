"""Module that tests the functionality of the pddl_precondition module."""
from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain, construct_expression_tree, NumericalExpressionTree, Predicate
from pddl_plus_parser.models.pddl_function import PDDLFunction
from pddl_plus_parser.models.pddl_precondition import Precondition
from tests.models_tests.consts import TEST_HARD_NUMERIC_DOMAIN, HARD_TEST_NUMERIC_DOMAIN, \
    DOMAIN_TO_TEST_INEQUALITY_REMOVAL, DOMAIN_TO_TEST_BOTH_TYPES_OF_INEQUALITY


@fixture()
def domain() -> Domain:
    domain_parser = DomainParser(TEST_HARD_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def complex_numeric_domain() -> Domain:
    domain_parser = DomainParser(HARD_TEST_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def domain_to_test_linear_inequality_removal() -> Domain:
    domain_parser = DomainParser(DOMAIN_TO_TEST_INEQUALITY_REMOVAL)
    return domain_parser.parse_domain()


@fixture()
def zenotravel_two_types_inequality_domain() -> Domain:
    domain_parser = DomainParser(DOMAIN_TO_TEST_BOTH_TYPES_OF_INEQUALITY)
    return domain_parser.parse_domain()


@fixture()
def simple_precondition() -> Precondition:
    return Precondition("and")


def test_add_condition_adds_a_single_predicate_correctly(simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)
    assert str(simple_precondition) == "(and (on_board ?i ?s))"


def test_add_condition_when_given_the_same_predicate_twice_does_not_add_it_a_second_time(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)
    simple_precondition.add_condition(test_predicate)
    assert str(simple_precondition) == "(and (on_board ?i ?s))"


def test_add_condition_with_nested_preconditions_keeps_both_copies_of_the_predicates(
        simple_precondition: Precondition, domain: Domain):
    test_predicate1 = domain.predicates["on_board"]
    test_predicate2 = domain.predicates["supports"]
    negative_predicate = test_predicate1.copy()
    negative_predicate.is_positive = False

    nested_condition = Precondition("or")
    nested_condition.add_condition(negative_predicate)
    nested_condition.add_condition(test_predicate2)
    simple_precondition.add_condition(test_predicate2)
    simple_precondition.add_condition(nested_condition)

    assert str(simple_precondition).count("(supports ?i ?m)") == 2
    assert str(simple_precondition).count("(on_board ?i ?s)") == 1


def test_eq_returns_true_for_unnested_preconditions_when_they_contain_a_single_predicate(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)

    other_precondition = Precondition("and")
    other_precondition.add_condition(test_predicate)

    assert simple_precondition == other_precondition


def test_eq_returns_true_for_unnested_preconditions_when_they_contain_a_predicate_and_a_numeric_expression(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    numeric_condition_expression = [">=", ["fuel", "?s"], ["slew_time", "?d_new", "?d_prev"]]
    numeric_expression = NumericalExpressionTree(
        construct_expression_tree(numeric_condition_expression, domain.functions))
    simple_precondition.add_condition(test_predicate)
    simple_precondition.add_condition(numeric_expression)

    other_precondition = Precondition("and")
    other_precondition.add_condition(test_predicate)
    other_precondition.add_condition(numeric_expression)

    assert simple_precondition == other_precondition


def test_eq_returns_false_for_unnested_preconditions_when_they_contain_a_predicate_and_a_numeric_expression_if_boolean_op_is_not_equal(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    numeric_condition_expression = [">=", ["fuel", "?s"], ["slew_time", "?d_new", "?d_prev"]]
    numeric_expression = NumericalExpressionTree(
        construct_expression_tree(numeric_condition_expression, domain.functions))
    simple_precondition.add_condition(test_predicate)
    simple_precondition.add_condition(numeric_expression)

    other_precondition = Precondition("or")
    other_precondition.add_condition(test_predicate)
    other_precondition.add_condition(numeric_expression)

    assert not simple_precondition == other_precondition


def test_remove_condition_returns_true_and_removes_precondition_from_a_non_nested_precondition_that_includes_only_predicates(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)
    assert test_predicate in simple_precondition.operands

    assert simple_precondition.remove_condition(test_predicate)
    assert test_predicate not in simple_precondition.operands


def test_remove_condition_returns_false_when_predicate_not_in_non_nested_precondition_that_includes_only_predicates(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    test_predicate_to_remove = domain.predicates["power_avail"]
    simple_precondition.add_condition(test_predicate)
    assert test_predicate in simple_precondition.operands
    assert test_predicate_to_remove not in simple_precondition.operands

    assert not simple_precondition.remove_condition(test_predicate_to_remove)


def test_remove_condition_returns_true_and_removes_precondition_from_a_non_nested_precondition_that_a_precondition(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    test_predicate_to_remove = domain.predicates["power_avail"]
    test_predicate_to_remove2 = domain.predicates["power_on"]
    simple_precondition.add_condition(test_predicate)
    test_inner_precondition = Precondition("and")
    test_inner_precondition.add_condition(test_predicate_to_remove)
    test_inner_precondition.add_condition(test_predicate_to_remove2)
    simple_precondition.add_condition(test_inner_precondition)
    assert test_predicate in simple_precondition.operands
    assert test_inner_precondition in simple_precondition.operands

    assert simple_precondition.remove_condition(test_inner_precondition)
    assert test_inner_precondition not in simple_precondition.operands


def test_contains_when_item_inside_a_non_nested_precondition_returns_true(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)
    assert test_predicate in simple_precondition


def test_contains_when_item_not_inside_a_non_nested_precondition_returns_false(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    test_predicate_to_remove = domain.predicates["power_avail"]
    simple_precondition.add_condition(test_predicate)
    assert test_predicate in simple_precondition
    assert test_predicate_to_remove not in simple_precondition


def test_contains_when_item_inside_a_nested_precondition_returns_true(
        simple_precondition: Precondition, domain: Domain):
    outer_predicate = domain.predicates["on_board"]
    inner_predicate = domain.predicates["power_avail"]
    tested_predicate = domain.predicates["power_on"]
    simple_precondition.add_condition(outer_predicate)
    test_inner_precondition = Precondition("and")
    test_inner_precondition.add_condition(inner_predicate)
    test_inner_precondition.add_condition(tested_predicate)
    simple_precondition.add_condition(test_inner_precondition)
    assert tested_predicate in simple_precondition


def test_print_with_simplify_option_on_numeric_condition_reduces_the_size_of_the_preconditions_compared_to_the_original(
        complex_numeric_domain: Domain):
    tested_action = complex_numeric_domain.actions["walk"]
    precondition = tested_action.preconditions
    original_preconditions = precondition.print(should_simplify=False)
    simplified_precondition = precondition.print(should_simplify=True)
    print(simplified_precondition)
    assert len(simplified_precondition) < len(original_preconditions)


def test_print_with_simplify_option_on_numeric_condition_reduces_the_size_of_the_preconditions_compared_to_the_original_even_when_the_removed_conditions_are_not_minimal(
        domain_to_test_linear_inequality_removal: Domain):
    tested_action = domain_to_test_linear_inequality_removal.actions["drive-truck"]
    precondition = tested_action.preconditions
    original_preconditions = precondition.print(should_simplify=False)
    simplified_precondition = precondition.print(should_simplify=True)
    print(simplified_precondition)
    assert len(simplified_precondition) < len(original_preconditions)


def test_print_with_simplify_option_on_numeric_condition_when_equality_condition_is_in_format_a_equals_b_returns_simplified_precondition_and_does_not_crash(
        domain_to_test_linear_inequality_removal: Domain):
    tested_action = domain_to_test_linear_inequality_removal.actions["walk"]
    precondition = tested_action.preconditions
    original_preconditions = precondition.print(should_simplify=False)
    try:
        simplified_precondition = precondition.print(should_simplify=True)
        print(simplified_precondition)
        assert len(simplified_precondition) <= len(original_preconditions)

    except Exception as e:
        assert False


def test_print_with_simplify_option_on_when_there_are_two_types_of_inequalities_returns_correct_condition_and_does_not_break_correctness(
        zenotravel_two_types_inequality_domain: Domain):
    tested_action = zenotravel_two_types_inequality_domain.actions["board"]
    precondition = tested_action.preconditions
    original_preconditions = precondition.print(should_simplify=False)
    simplified_precondition = precondition.print(should_simplify=True)
    print(simplified_precondition)
    assert len(simplified_precondition) == len(original_preconditions)
    assert "(<= (onboard ?a) 6)" in simplified_precondition
    assert "(>= (onboard ?a) 0)" in simplified_precondition


def test_change_signature_with_complex_action_returns_precondition_with_correct_parameter_names(
        zenotravel_two_types_inequality_domain: Domain):
    tested_action = zenotravel_two_types_inequality_domain.actions["board"]
    precondition = tested_action.preconditions
    old_to_new_param_names = {action_param: f"?param_{i}" for i, action_param in
                              enumerate(tested_action.signature.keys())}
    precondition.change_signature(old_to_new_param_names)
    for _, precond in precondition:
        if isinstance(precond, Predicate):
            assert set(precond.signature.keys()).issubset(set(old_to_new_param_names.values()))

        if isinstance(precond, NumericalExpressionTree):
            for item in precond:
                if isinstance(item, PDDLFunction):
                    assert set(item.signature.keys()).issubset(set(old_to_new_param_names.values()))


def test_change_signature_with_complex_action_returns_precondition_with_correct_parameter_names_when_preconditions_contain_equality_condition(
        zenotravel_two_types_inequality_domain: Domain):
    tested_action = zenotravel_two_types_inequality_domain.actions["board"]
    precondition = tested_action.preconditions
    old_to_new_param_names = {action_param: f"?param_{i}" for i, action_param in
                              enumerate(tested_action.signature.keys())}
    precondition.root.add_equality_condition(("?a", "?c"))
    precondition.change_signature(old_to_new_param_names)
    assert precondition.root.equality_preconditions == {("?param_1", "?param_2")}
