"""Module test for the grounded operator class."""
from typing import List, Dict, Set

from pytest import fixture, raises, fail

from lisp_parsers import DomainParser
from models import Domain, Action, Operator, GroundedPredicate, PDDLFunction, State
from tests.models_tests.consts import TEST_HARD_NUMERIC_DOMAIN

TEST_LIFTED_SIGNATURE_ITEMS = ["?s", "?d", "?i", "?m"]
TEST_GROUNDED_ACTION_CALL = ["s1", "test_direction", "test_instrument", "test_mode"]


@fixture()
def domain() -> Domain:
    domain_parser = DomainParser(TEST_HARD_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def numeric_action(domain: Domain) -> Action:
    return domain.actions["take_image"]


@fixture()
def operator(domain: Domain, numeric_action: Action) -> Operator:
    return Operator(numeric_action, domain, TEST_GROUNDED_ACTION_CALL)


@fixture()
def complete_state_predicates(domain: Domain) -> Dict[str, Set[GroundedPredicate]]:
    calibrated_predicate = domain.predicates["calibrated"]
    on_board_predicate = domain.predicates["on_board"]
    supports_predicate = domain.predicates["supports"]
    power_on_predicate = domain.predicates["power_on"]
    pointing_predicate = domain.predicates["pointing"]
    return {
        "(calibrated ?i)": {
            GroundedPredicate(name="calibrated", signature=calibrated_predicate.signature,
                              object_mapping={"?i": "test_instrument"})},
        "(on_board ?i ?s)": [
            GroundedPredicate(name="on_board", signature=on_board_predicate.signature,
                              object_mapping={"?i": "test_instrument", "?s": "s1"})],
        "(supports ?i ?m)": {
            GroundedPredicate(name="supports", signature=supports_predicate.signature,
                              object_mapping={"?i": "test_instrument", "?m": "test_mode"})},
        "(power_on ?i)": {
            GroundedPredicate(name="power_on", signature=power_on_predicate.signature,
                              object_mapping={"?i": "test_instrument"})},
        "(pointing ?s ?d)": {
            GroundedPredicate(name="pointing", signature=pointing_predicate.signature,
                              object_mapping={"?s": "s1", "?d": "test_direction"})},
    }


@fixture()
def numeric_state_variables(domain: Domain) -> Dict[str, PDDLFunction]:
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    return {
        data_capacity_function.untyped_representation: data_capacity_function,
        data_function.untyped_representation: data_function,
    }


@fixture()
def previous_state_with_missing_numeric_fluent(domain: Domain,
                                               complete_state_predicates: Dict[str, Set[GroundedPredicate]],
                                               numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(18.3)
    numeric_state_variables[data_function.untyped_representation].set_value(5.3)
    return State(predicates=complete_state_predicates, fluents=numeric_state_variables)


@fixture()
def valid_previous_state(domain: Domain,
                         complete_state_predicates: Dict[str, Set[GroundedPredicate]],
                         numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    data_stored_function = PDDLFunction(name="data-stored", signature={})
    data_stored_function.set_value(10)
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(18.3)
    numeric_state_variables[data_function.untyped_representation].set_value(5.3)
    return State(predicates=complete_state_predicates, fluents={
        **numeric_state_variables,
        data_stored_function.untyped_representation: data_stored_function
    })


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


def test_ground_grounds_positive_preconditions_with_correct_objects(operator: Operator):
    operator.ground()
    positive_grounded_preconditions = operator.grounded_positive_preconditions

    expected_grounded_preconditions = ['(on_board test_instrument s1)',
                                       '(power_on test_instrument)',
                                       '(pointing s1 test_direction)',
                                       '(calibrated test_instrument)',
                                       '(supports test_instrument test_mode)']

    assert len(positive_grounded_preconditions) == len(expected_grounded_preconditions)
    assert sorted([p.untyped_representation for p in positive_grounded_preconditions]) == sorted(
        expected_grounded_preconditions)


def test_ground_grounds_negative_preconditions_with_correct_objects(operator: Operator):
    operator.ground()
    positive_grounded_preconditions = operator.grounded_negative_preconditions

    expected_grounded_preconditions = []
    assert len(positive_grounded_preconditions) == len(expected_grounded_preconditions)


def test_ground_grounds_numeric_preconditions_with_correct_objects(operator: Operator):
    operator.ground()
    positive_grounded_numeric_preconditions = operator.grounded_numeric_preconditions

    assert len(positive_grounded_numeric_preconditions) == 1
    numeric_expression = positive_grounded_numeric_preconditions.pop()

    root = numeric_expression.root
    assert root.id == ">="
    assert root.children[0].id == "(data_capacity s1 - satellite)"
    assert root.children[1].id == "(data test_direction - direction test_mode - mode)"


def test_ground_grounds_numeric_effects_with_correct_objects(operator: Operator):
    operator.ground()
    positive_grounded_numeric_effects = operator.grounded_numeric_effects

    assert len(positive_grounded_numeric_effects) == 2

    first_expression = positive_grounded_numeric_effects.pop()
    second_expression = positive_grounded_numeric_effects.pop()

    expression_map = {
        first_expression.root.id: first_expression.root,
        second_expression.root.id: second_expression.root
    }

    root = expression_map["decrease"]
    assert root.children[0].id == "(data_capacity s1 - satellite)"
    assert root.children[1].id == "(data test_direction - direction test_mode - mode)"

    root = expression_map["increase"]
    assert root.children[0].id == "(data-stored )"
    assert root.children[1].id == "(data test_direction - direction test_mode - mode)"


def test_ground_grounds_boolean_effects_with_correct_objects(operator: Operator):
    operator.ground()
    grounded_add_effects = operator.grounded_add_effects

    assert len(grounded_add_effects) == 1
    expected_grounded_add_effect = ['(have_image test_direction test_mode)']
    assert [p.untyped_representation for p in grounded_add_effects] == expected_grounded_add_effect
    assert len(operator.grounded_delete_effects) == 0


def test_is_applicable_return_false_when_one_predicate_missing_in_state_predicates(
        operator: Operator, domain: Domain, complete_state_predicates: Dict[str, List[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)

    missing_predicate_state_variables = {**complete_state_predicates}
    missing_predicate_state_variables.pop("(calibrated ?i)")

    state_with_missing_predicate = State(predicates=missing_predicate_state_variables, fluents=numeric_state_variables)
    assert not operator.is_applicable(state_with_missing_predicate)


def test_is_applicable_return_true_when_all_predicates_are_present_in_the_state(
        operator: Operator, domain: Domain, complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert operator.is_applicable(state_with_complete_predicates)


def test_is_applicable_return_false_when_numeric_fluents_dont_correspond_preconditions_requirements(
        operator: Operator, domain: Domain, complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)
    numeric_state_variables[data_function.untyped_representation].set_value(18.7)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert not operator.is_applicable(state_with_complete_predicates)


def test_is_applicable_return_true_when_numeric_fluents_are_equal(
        operator: Operator, domain: Domain, complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)
    numeric_state_variables[data_function.untyped_representation].set_value(5.3)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert operator.is_applicable(state_with_complete_predicates)


def test_is_applicable_return_true_when_given_correct_fluents_with_negative_values(
        operator: Operator, domain: Domain, complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(-5.3)
    numeric_state_variables[data_function.untyped_representation].set_value(-15.32)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert operator.is_applicable(state_with_complete_predicates)


def test_update_state_functions_raises_error_when_a_function_is_missing_in_previous_state(
        operator: Operator, previous_state_with_missing_numeric_fluent: State):
    with raises(ValueError):
        operator.ground()
        operator.update_state_functions(previous_state_with_missing_numeric_fluent)

def test_update_state_functions_does_not_raise_error_when_all_functions_are_present_in_state(
        operator: Operator, valid_previous_state: State):
    try:
        operator.ground()
        operator.update_state_functions(valid_previous_state)
    except Exception:
        fail()

def test_update_state_functions_returns_state_variables_with_correct_new_values(
        domain: Domain, operator: Operator, valid_previous_state: State):
    operator.ground()
    new_state_numeric_fluents = operator.update_state_functions(valid_previous_state)

    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    data_stored_function = PDDLFunction(name="data-stored", signature={})

    assert new_state_numeric_fluents[data_function.untyped_representation].value == 5.3
    assert new_state_numeric_fluents[data_capacity_function.untyped_representation].value == 18.3 - 5.3
    assert new_state_numeric_fluents[data_stored_function.untyped_representation].value == 10 + 5.3


def test_update_state_functions_does_not_add_redundant_numeric_state_variables(
        operator: Operator, valid_previous_state: State):
    operator.ground()
    new_state_numeric_fluents = operator.update_state_functions(valid_previous_state)

    assert len(new_state_numeric_fluents) == 3

def test_update_state_predicates_adds_new_predicate_to_the_new_state(
        operator: Operator, valid_previous_state: State):
    operator.ground()
    new_state_predicates = operator.update_state_predicates(valid_previous_state)

    assert len(new_state_predicates) == len(valid_previous_state.state_predicates) + 1

def test_update_state_predicates_adds_the_correct_predicate(
        operator: Operator, valid_previous_state: State):
    operator.ground()
    new_state_predicates = operator.update_state_predicates(valid_previous_state)

    assert "(have_image ?d ?m)" in new_state_predicates

def test_update_state_predicates_removed_predicate_when_predicate_in_delete_effects(
        domain: Domain, operator: Operator, valid_previous_state: State):
    pointing_predicate_str = "(pointing ?s ?d)"
    assert len(valid_previous_state.state_predicates[pointing_predicate_str]) == 1
    pointing_predicate = domain.predicates["pointing"]

    operator.ground()
    operator.grounded_delete_effects = {
            GroundedPredicate(name="pointing", signature=pointing_predicate.signature,
                              object_mapping={"?s": "s1", "?d": "test_direction"})}

    new_state_predicates = operator.update_state_predicates(valid_previous_state)

    assert len(new_state_predicates[pointing_predicate_str]) == 0

def test_apply_returns_new_state_with_correct_values(
        domain: Domain, operator: Operator, valid_previous_state: State):
    next_state = operator.apply(valid_previous_state)
    next_state_fluents = next_state.state_fluents
    next_state_predicates = next_state.state_predicates

    assert "(have_image ?d ?m)" in next_state_predicates
    assert len(next_state_fluents) == 3
    data_function = PDDLFunction(name="data", signature={
        "test_direction": domain.types["direction"],
        "test_mode": domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": domain.types["satellite"]})
    data_stored_function = PDDLFunction(name="data-stored", signature={})

    assert next_state_fluents[data_function.untyped_representation].value == 5.3
    assert next_state_fluents[data_capacity_function.untyped_representation].value == 18.3 - 5.3
    assert next_state_fluents[data_stored_function.untyped_representation].value == 10 + 5.3