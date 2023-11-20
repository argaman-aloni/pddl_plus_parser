"""Module to test the functionality of grounded effects."""
from typing import Dict, Set

from pytest import fixture, fail, raises

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Domain, Action, GroundedPredicate, PDDLFunction, State, Problem
from pddl_plus_parser.models.grounded_effect import GroundedEffect
from tests.lisp_parsers_tests.consts import SPIDER_PROBLEM_PATH
from tests.models_tests.consts import TEST_HARD_NUMERIC_DOMAIN, TEST_NUMERIC_DOMAIN, SPIDER_DOMAIN_PATH, \
    NURIKABE_DOMAIN_PATH, NURIKABE_PROBLEM_PATH, MINECRAFT_LARGE_DOMAIN_PATH, MINECRAFT_LARGE_PROBLEM_PATH

TEST_LIFTED_SIGNATURE_ITEMS = ["?s", "?d", "?i", "?m"]
TEST_GROUNDED_ACTION_CALL = ["s1", "test_direction", "test_instrument", "test_mode"]

AGRICOLA_LIFTED_SIGNATURE_ITEMS = ["?w1", "?w2", "?wmax", "?r", "?i1", "?i2"]
AGRICOLA_GROUNDED_ACTION_CALL = ["noworker", "w1", "w2", "round1", "n1", "n2"]

SPIDER_START_DEALING_CALL = []
SPIDER_DEAL_CARD_CALL = ["card-d0-s1-v3", "card-d0-s0-v3", "deal-0", "card-d0-s3-v1", "pile-0"]
NURIKABE_START_PAINTING_CALL = ["pos-0-0", "g0", "n1", "n0"]
NURIKABE_MOVE_PAINTING_CALL = ["pos-2-0", "pos-3-0", "g1", "n1", "n0"]


@fixture()
def satellite_domain() -> Domain:
    domain_parser = DomainParser(TEST_HARD_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def agricola_domain() -> Domain:
    domain_parser = DomainParser(TEST_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def spider_domain() -> Domain:
    domain_parser = DomainParser(SPIDER_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def nurikabe_domain() -> Domain:
    domain_parser = DomainParser(NURIKABE_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def minecraft_large_domain() -> Domain:
    domain_parser = DomainParser(MINECRAFT_LARGE_DOMAIN_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def spider_problem(spider_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SPIDER_PROBLEM_PATH, domain=spider_domain).parse_problem()


@fixture()
def nurikabe_problem(nurikabe_domain: Domain) -> Problem:
    return ProblemParser(problem_path=NURIKABE_PROBLEM_PATH, domain=nurikabe_domain).parse_problem()


@fixture()
def take_image_numeric_action(satellite_domain: Domain) -> Action:
    return satellite_domain.actions["take_image"]


@fixture()
def agricola_numeric_action(agricola_domain: Domain) -> Action:
    return agricola_domain.actions["take_food"]


@fixture()
def spider_unconditional_action(spider_domain: Domain) -> Action:
    return spider_domain.actions["start-dealing"]


@fixture()
def spider_conditional_action(spider_domain: Domain) -> Action:
    return spider_domain.actions["deal-card"]


@fixture()
def nurikabe_unconditional_action(nurikabe_domain: Domain) -> Action:
    return nurikabe_domain.actions["start-painting"]


@fixture()
def nurikabe_conditional_action(nurikabe_domain: Domain) -> Action:
    return nurikabe_domain.actions["move-painting"]


@fixture()
def satellite_action_effects(satellite_domain: Domain, take_image_numeric_action: Action) -> GroundedEffect:
    return GroundedEffect(None, take_image_numeric_action.discrete_effects, take_image_numeric_action.numeric_effects,
                          satellite_domain, take_image_numeric_action)


@fixture()
def numeric_state_variables(satellite_domain: Domain) -> Dict[str, PDDLFunction]:
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    return {
        data_capacity_function.untyped_representation: data_capacity_function,
        data_function.untyped_representation: data_function,
    }


@fixture()
def complete_state_predicates(satellite_domain: Domain) -> Dict[str, Set[GroundedPredicate]]:
    calibrated_predicate = satellite_domain.predicates["calibrated"]
    on_board_predicate = satellite_domain.predicates["on_board"]
    supports_predicate = satellite_domain.predicates["supports"]
    power_on_predicate = satellite_domain.predicates["power_on"]
    pointing_predicate = satellite_domain.predicates["pointing"]
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
def previous_state_with_missing_numeric_fluent(satellite_domain: Domain,
                                               complete_state_predicates: Dict[str, Set[GroundedPredicate]],
                                               numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(18.3)
    numeric_state_variables[data_function.untyped_representation].set_value(5.3)
    return State(predicates=complete_state_predicates, fluents=numeric_state_variables)


@fixture()
def minecraft_large_problem(minecraft_large_domain: Domain) -> Problem:
    return ProblemParser(problem_path=MINECRAFT_LARGE_PROBLEM_PATH, domain=minecraft_large_domain).parse_problem()


@fixture()
def valid_previous_state(satellite_domain: Domain,
                         complete_state_predicates: Dict[str, Set[GroundedPredicate]],
                         numeric_state_variables: Dict[str, PDDLFunction]):
    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    data_stored_function = PDDLFunction(name="data-stored", signature={})
    data_stored_function.set_value(10)
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(18.3)
    numeric_state_variables[data_function.untyped_representation].set_value(5.3)
    return State(predicates=complete_state_predicates, fluents={
        **numeric_state_variables,
        data_stored_function.untyped_representation: data_stored_function
    })


def test_ground_conditional_effect_grounds_numeric_effects_with_correct_objects(
        satellite_action_effects: GroundedEffect):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    positive_grounded_numeric_effects = satellite_action_effects.grounded_numeric_effects

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


def test_ground_grounds_boolean_effects_with_correct_objects(satellite_action_effects: GroundedEffect):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    grounded_add_effects = [effect for effect in satellite_action_effects.grounded_discrete_effects
                            if effect.is_positive]

    grounded_delete_effects = [effect for effect in satellite_action_effects.grounded_discrete_effects
                               if not effect.is_positive]

    assert len(grounded_add_effects) == 1
    expected_grounded_add_effect = ['(have_image test_direction test_mode)']
    assert [p.untyped_representation for p in grounded_add_effects] == expected_grounded_add_effect
    assert len(grounded_delete_effects) == 0


def test_antecedents_hold_for_non_conditional_action_returns_true_in_valid_state(
        satellite_action_effects: GroundedEffect, valid_previous_state: State):
    assert satellite_action_effects.antecedents_hold(valid_previous_state)


def test_antecedents_hold_for_non_conditional_action_returns_true_in_invalid_state(
        satellite_action_effects: GroundedEffect, previous_state_with_missing_numeric_fluent: State):
    assert satellite_action_effects.antecedents_hold(previous_state_with_missing_numeric_fluent)


def test_apply_does_not_raise_error_when_all_functions_are_present_in_state(
        satellite_action_effects: GroundedEffect, valid_previous_state: State):
    try:
        test_parameters_map = {
            lifted_param: grounded_object for lifted_param, grounded_object in zip(
                TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
        }
        satellite_action_effects.ground_conditional_effect(test_parameters_map)
        satellite_action_effects.apply(valid_previous_state)
    except Exception:
        fail()


def test_apply_raises_error_when_all_functions_are_present_in_state(
        satellite_action_effects: GroundedEffect, valid_previous_state: State):
    with raises(KeyError):
        test_parameters_map = {
            lifted_param: grounded_object for lifted_param, grounded_object in zip(
                TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
        }
        satellite_action_effects.ground_conditional_effect(test_parameters_map)
        del valid_previous_state.state_fluents["(data_capacity ?s)"]
        satellite_action_effects.apply(valid_previous_state)


def test_apply_returns_state_variables_with_correct_new_values(
        satellite_action_effects: GroundedEffect, satellite_domain: Domain, valid_previous_state: State):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    tmp_state = valid_previous_state.copy()
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    satellite_action_effects.apply(tmp_state)
    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    data_stored_function = PDDLFunction(name="data-stored", signature={})

    new_state_numeric_fluents = tmp_state.state_fluents
    assert new_state_numeric_fluents[data_function.untyped_representation].value == 5.3
    assert new_state_numeric_fluents[data_capacity_function.untyped_representation].value == 18.3 - 5.3
    assert new_state_numeric_fluents[data_stored_function.untyped_representation].value == 10 + 5.3


def test_apply_does_not_add_redundant_numeric_state_variables(
        satellite_action_effects: GroundedEffect, valid_previous_state: State):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    tmp_state = valid_previous_state.copy()
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    satellite_action_effects.apply(tmp_state)
    new_state_numeric_fluents = tmp_state.state_fluents

    assert len(new_state_numeric_fluents) == 3


def test_apply_adds_new_predicate_to_the_new_state(
        satellite_action_effects: GroundedEffect, valid_previous_state: State):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    tmp_state = valid_previous_state.copy()
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    new_state_predicates = tmp_state.state_predicates
    satellite_action_effects.apply(tmp_state)
    assert len(new_state_predicates) == len(valid_previous_state.state_predicates) + 1


def test_apply_adds_the_correct_predicate(satellite_action_effects: GroundedEffect, valid_previous_state: State):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    tmp_state = valid_previous_state.copy()
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    new_state_predicates = tmp_state.state_predicates
    satellite_action_effects.apply(tmp_state)

    assert "(have_image ?d ?m)" in new_state_predicates


def test_apply_removed_predicate_when_predicate_in_delete_effects(
        satellite_domain: Domain, satellite_action_effects: GroundedEffect, valid_previous_state: State):
    pointing_predicate_str = "(pointing ?s ?d)"
    assert len(valid_previous_state.state_predicates[pointing_predicate_str]) == 1
    pointing_predicate = satellite_domain.predicates["pointing"]

    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_effects.grounded_discrete_effects = {
        GroundedPredicate(name="pointing", signature=pointing_predicate.signature,
                          object_mapping={"?s": "s1", "?d": "test_direction"}, is_positive=False)}

    tmp_state = valid_previous_state.copy()
    satellite_action_effects.ground_conditional_effect(test_parameters_map)
    new_state_predicates = tmp_state.state_predicates
    satellite_action_effects.apply(tmp_state)
    assert len(new_state_predicates[pointing_predicate_str]) == 0


def test_apply_uses_delete_then_add_methodology_and_does_not_remove_predicates_that_should_appear_in_state(
        minecraft_large_problem: Problem, minecraft_large_domain: Domain):
    state_predicates = minecraft_large_problem.initial_state_predicates
    state_fluents = minecraft_large_problem.initial_state_fluents
    initial_state = State(predicates=state_predicates, fluents=state_fluents, is_init=True)
    minecraft_grounded_effect = GroundedEffect(
        None,
        minecraft_large_domain.actions["tp_to"].discrete_effects,
        minecraft_large_domain.actions["tp_to"].numeric_effects,
        minecraft_large_domain,
        minecraft_large_domain.actions["tp_to"])
    minecraft_grounded_effect.ground_conditional_effect({"?from": "cell15", "?to": "cell15"})
    new_state = initial_state.copy()
    minecraft_grounded_effect.apply(new_state)
    assert "(position cell15)" in new_state.serialize()
