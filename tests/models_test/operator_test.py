"""Module test for the grounded operator class."""
from pytest import fixture, raises, fail

from lisp_parsers import DomainParser
from models import Domain, Action, Operator
from tests.models_test.consts import TEST_HARD_NUMERIC_DOMAIN

TEST_LIFTED_SIGNATURE_ITEMS = ["?s", "?d", "?i", "?m"]
TEST_GROUNDED_ACTION_CALL = ["s1", "test_direction", "test_instrument", "test_mode"]


@fixture(scope="module")
def domain() -> Domain:
    domain_parser = DomainParser(TEST_HARD_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def numeric_action(domain: Domain) -> Action:
    return domain.actions["take_image"]


@fixture()
def operator(domain: Domain, numeric_action: Action) -> Operator:
    return Operator(numeric_action, domain, TEST_GROUNDED_ACTION_CALL)


def test_ground_predicates_creates_grounded_version_of_lifted_predicates_with_object_names_in_the_parameters(
        operator: Operator, numeric_action: Action):
    test_lifted_predicates = numeric_action.positive_preconditions
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    grounded_predicates = operator.ground_predicates(lifted_predicates=test_lifted_predicates,
                                                     parameters_map=test_parameters_map)

    expected_grounded_preconditions = ['(on_board test_instrument s1)',
                                       '(power_on test_instrument)',
                                       '(pointing s1 test_direction)',
                                       '(calibrated test_instrument)',
                                       '(supports test_instrument test_mode)']
    assert len(grounded_predicates) == len(test_lifted_predicates)
    assert sorted([p.untyped_representation for p in grounded_predicates]) == sorted(expected_grounded_preconditions)


def test_ground_predicates_creates_grounded_version_of_lifted_predicates_with_correct_parameter_mapping(
        operator: Operator, numeric_action: Action):
    test_lifted_predicates = numeric_action.positive_preconditions
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    grounded_predicates = operator.ground_predicates(lifted_predicates=test_lifted_predicates,
                                                     parameters_map=test_parameters_map)

    for predicate in grounded_predicates:
        if predicate.name == "calibrated":
            assert predicate.object_mapping == {"?i": "test_instrument"}


def test_ground_numeric_calculation_tree_extracts_correct_grounded_tree_data_from_lifted_calc_tree(operator: Operator,
                                                                                                   numeric_action: Action):
    test_lifted_expression_tree = numeric_action.numeric_preconditions.pop()
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }

    expression_tree = operator.ground_numeric_calculation_tree(test_lifted_expression_tree, test_parameters_map)

    root = expression_tree.root
    assert root.id == ">="
    assert root.children[0].id == "(data_capacity s1 - satellite)"
    assert root.children[1].id == "(data test_direction - direction test_mode - mode)"


def test_ground_numeric_expressions_extracts_all_numeric_expressions(operator: Operator, numeric_action: Action):
    test_lifted_expression_tree = numeric_action.numeric_effects
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }

    expression_tree_set = operator.ground_numeric_expressions(test_lifted_expression_tree, test_parameters_map)

    assert len(expression_tree_set) == 2
