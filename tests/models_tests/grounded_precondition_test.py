"""Module test for the grounded precondition class."""
from typing import Dict, Set, List

from pytest import fixture, fail

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, PDDLTokenizer, TrajectoryParser
from pddl_plus_parser.models import Domain, Action, GroundedPredicate, PDDLFunction, State, Problem, Precondition, \
    NumericalExpressionTree, Observation
from pddl_plus_parser.models.grounded_precondition import GroundedPrecondition
from tests.lisp_parsers_tests.consts import SPIDER_PROBLEM_PATH
from tests.models_tests.consts import TEST_HARD_NUMERIC_DOMAIN, TEST_NUMERIC_DOMAIN, SPIDER_DOMAIN_PATH, \
    NURIKABE_DOMAIN_PATH, NURIKABE_PROBLEM_PATH, MICONIC_NESTED_DOMAIN_PATH, MICONIC_NESTED_PROBLEM_PATH, \
    MICONIC_DOMAIN_PATH, MICONIC_TRAJECTORY_PATH

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
def miconic_nested_domain() -> Domain:
    domain_parser = DomainParser(MICONIC_NESTED_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def miconic_domain() -> Domain:
    domain_parser = DomainParser(MICONIC_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def spider_problem(spider_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SPIDER_PROBLEM_PATH, domain=spider_domain).parse_problem()


@fixture()
def nurikabe_problem(nurikabe_domain: Domain) -> Problem:
    return ProblemParser(problem_path=NURIKABE_PROBLEM_PATH, domain=nurikabe_domain).parse_problem()


@fixture()
def miconic_nested_problem(miconic_domain: Domain) -> Problem:
    return ProblemParser(problem_path=MICONIC_NESTED_PROBLEM_PATH, domain=miconic_domain).parse_problem()


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
def miconic_stop_action(miconic_nested_domain: Domain) -> Action:
    return miconic_nested_domain.actions["stop"]


@fixture()
def satellite_action_precondition(satellite_domain: Domain, take_image_numeric_action: Action) -> GroundedPrecondition:
    return GroundedPrecondition(take_image_numeric_action.preconditions, satellite_domain, take_image_numeric_action)


@fixture()
def agricola_action_precondition(agricola_domain: Domain, agricola_numeric_action: Action) -> GroundedPrecondition:
    return GroundedPrecondition(agricola_numeric_action.preconditions, agricola_domain, agricola_numeric_action)


@fixture()
def spider_action_precondition(spider_domain: Domain, spider_conditional_action: Action) -> GroundedPrecondition:
    return GroundedPrecondition(spider_conditional_action.preconditions, spider_domain, spider_conditional_action)


@fixture()
def miconic_stop_action_precondition(miconic_nested_domain: Domain,
                                     miconic_stop_action: Action) -> GroundedPrecondition:
    return GroundedPrecondition(miconic_stop_action.preconditions, miconic_nested_domain, miconic_stop_action)


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


@fixture()
def miconic_observation(miconic_domain: Domain, miconic_nested_problem: Problem) -> Observation:
    return TrajectoryParser(miconic_domain, miconic_nested_problem).parse_trajectory(MICONIC_TRAJECTORY_PATH)


def test_ground_equality_objects_returns_correct_grounded_objects(satellite_action_precondition: GroundedPrecondition):
    equality_precondition = {("?size_before", "?size_after")}
    parameter_map = {"?size_before": "size1", "?size_after": "size2"}
    grounded_objects = satellite_action_precondition._ground_equality_objects(equality_precondition, parameter_map)
    assert grounded_objects == {("size1", "size2")}


def test_equality_holds_when_objects_not_equal_returns_false(satellite_action_precondition: GroundedPrecondition):
    test_precondition = Precondition("and")
    test_precondition.equality_preconditions = {("size1", "size2")}
    assert not satellite_action_precondition._validate_equality_holds(test_precondition)


def test_equality_holds_when_not_all_objects_equal_returns_false(satellite_action_precondition: GroundedPrecondition):
    test_precondition = Precondition("and")
    test_precondition.equality_preconditions = {("size1", "size1"), ("size3", "size1")}
    assert not satellite_action_precondition._validate_equality_holds(test_precondition)


def test_equality_holds_when_objects_equal_returns_true(satellite_action_precondition: GroundedPrecondition):
    test_precondition = Precondition("and")
    test_precondition.equality_preconditions = {("size1", "size1")}
    assert satellite_action_precondition._validate_equality_holds(test_precondition)


def test_ground_preconditions_creates_grounded_version_of_lifted_predicates_with_object_names_in_the_parameters(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_preconditions = satellite_action_precondition._grounded_precondition
    expected_grounded_preconditions = ['(on_board test_instrument s1)',
                                       '(power_on test_instrument)',
                                       '(pointing s1 test_direction)',
                                       '(calibrated test_instrument)',
                                       '(supports test_instrument test_mode)']
    for precondition in expected_grounded_preconditions:
        assert precondition in str(grounded_preconditions)
    print(grounded_preconditions)


def test_ground_preconditions_creates_grounded_version_of_lifted_functions_with_correct_operators(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_preconditions = satellite_action_precondition._grounded_precondition
    expected_grounded_numeric_preconditions = ['(>= (data_capacity s1) (data test_direction test_mode))']
    for precondition in expected_grounded_numeric_preconditions:
        assert precondition in str(grounded_preconditions)


def test_ground_preconditions_when_domain_contains_constants_grounds_action_correctly(
        agricola_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            AGRICOLA_LIFTED_SIGNATURE_ITEMS, AGRICOLA_GROUNDED_ACTION_CALL)
    }
    agricola_action_precondition.ground_preconditions(test_parameters_map)
    grounded_preconditions = agricola_action_precondition._grounded_precondition
    expected_grounded_preconditions = ['(available_action act_labor)',
                                       '(current_worker noworker)',
                                       '(next_worker noworker w1)',
                                       '(max_worker w2)',
                                       '(current_round round1)',
                                       '(num_food n1)',
                                       '(next_num n1 n2)']
    for precondition in expected_grounded_preconditions:
        assert precondition in str(grounded_preconditions)
    print(grounded_preconditions)


def test_ground_preconditions_creates_grounded_predicates_with_correct_parameter_mapping(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_preconditions = satellite_action_precondition._grounded_precondition
    for _, precondition in grounded_preconditions:
        if isinstance(precondition, GroundedPredicate):
            for parameter in precondition.object_mapping:
                assert parameter in test_parameters_map
                assert test_parameters_map[parameter] == precondition.object_mapping[parameter]


def test_ground_preconditions_grounds_precondition_with_equality_conditions_correctly(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition._lifted_precondition.root.equality_preconditions = {("?i", "?s")}
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_preconditions = satellite_action_precondition._grounded_precondition
    expected_grounded_preconditions = ["(= test_instrument s1)"]
    for precondition in expected_grounded_preconditions:
        assert precondition in str(grounded_preconditions)


def test_ground_preconditions_grounds_precondition_with_inequality_conditions_correctly(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition._lifted_precondition.root.inequality_preconditions = {("?i", "?s")}
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_preconditions = satellite_action_precondition._grounded_precondition
    expected_grounded_preconditions = ["(not (= test_instrument s1))"]
    for precondition in expected_grounded_preconditions:
        assert precondition in str(grounded_preconditions)


def test_ground_preconditions_grounds_positive_preconditions_with_correct_objects(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_predicates = []
    for _, grounded_precondition in satellite_action_precondition._grounded_precondition:
        if isinstance(grounded_precondition, GroundedPredicate):
            grounded_predicates.append(grounded_precondition)

    expected_grounded_preconditions = ['(on_board test_instrument s1)',
                                       '(power_on test_instrument)',
                                       '(pointing s1 test_direction)',
                                       '(calibrated test_instrument)',
                                       '(supports test_instrument test_mode)']

    assert len(grounded_predicates) == len(expected_grounded_preconditions)
    assert sorted([p.untyped_representation for p in grounded_predicates]) == sorted(
        expected_grounded_preconditions)


def test_ground_preconditions_grounds_negative_preconditions_with_correct_objects(
        spider_action_precondition: GroundedPrecondition, spider_conditional_action: Action):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            spider_conditional_action.signature.keys(), SPIDER_DEAL_CARD_CALL)
    }
    spider_action_precondition.ground_preconditions(test_parameters_map)
    grounded_predicates = []
    for _, grounded_precondition in spider_action_precondition._grounded_precondition:
        if isinstance(grounded_precondition, GroundedPredicate) and not grounded_precondition.is_positive:
            grounded_predicates.append(grounded_precondition)

    expected_grounded_preconditions = ["(not (currently-updating-movable ))",
                                       "(not (currently-updating-unmovable ))",
                                       "(not (currently-updating-part-of-tableau ))",
                                       "(not (currently-collecting-deck ))"]

    assert len(grounded_predicates) == len(expected_grounded_preconditions)
    assert sorted([p.untyped_representation for p in grounded_predicates]) == sorted(
        expected_grounded_preconditions)


def test_ground_preconditions_grounds_numeric_preconditions_with_correct_objects(
        satellite_action_precondition: GroundedPrecondition):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    grounded_expression = []
    for _, grounded_precondition in satellite_action_precondition._grounded_precondition:
        if isinstance(grounded_precondition, NumericalExpressionTree):
            grounded_expression.append(grounded_precondition)

    numeric_expression = grounded_expression[0]
    root = numeric_expression.root
    assert root.id == ">="
    assert root.children[0].id == "(data_capacity s1 - satellite)"
    assert root.children[1].id == "(data test_direction - direction test_mode - mode)"


def test_is_applicable_return_false_when_one_predicate_missing_in_state_predicates(
        satellite_action_precondition: GroundedPrecondition, satellite_domain: Domain,
        complete_state_predicates: Dict[str, List[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)

    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)

    missing_predicate_state_variables = {**complete_state_predicates}
    missing_predicate_state_variables.pop("(calibrated ?i)")

    state_with_missing_predicate = State(predicates=missing_predicate_state_variables, fluents=numeric_state_variables)
    assert not satellite_action_precondition.is_applicable(state_with_missing_predicate)


def test_is_applicable_return_true_when_all_predicates_are_present_in_the_state(
        satellite_action_precondition: GroundedPrecondition, satellite_domain: Domain,
        complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert satellite_action_precondition.is_applicable(state_with_complete_predicates)


def test_is_applicable_return_false_when_numeric_fluents_dont_correspond_preconditions_requirements(
        satellite_action_precondition: GroundedPrecondition, satellite_domain: Domain,
        complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)
    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)
    numeric_state_variables[data_function.untyped_representation].set_value(18.7)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert not satellite_action_precondition.is_applicable(state_with_complete_predicates)


def test_is_applicable_return_true_when_numeric_fluents_are_equal(
        satellite_action_precondition: GroundedPrecondition, satellite_domain: Domain,
        complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)

    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(5.3)
    numeric_state_variables[data_function.untyped_representation].set_value(5.3)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert satellite_action_precondition.is_applicable(state_with_complete_predicates)


def test_is_applicable_return_true_when_given_correct_fluents_with_negative_values(
        satellite_action_precondition: GroundedPrecondition, satellite_domain: Domain,
        complete_state_predicates: Dict[str, Set[GroundedPredicate]],
        numeric_state_variables: Dict[str, PDDLFunction]):
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    satellite_action_precondition.ground_preconditions(test_parameters_map)

    data_function = PDDLFunction(name="data", signature={
        "test_direction": satellite_domain.types["direction"],
        "test_mode": satellite_domain.types["mode"]
    })
    data_capacity_function = PDDLFunction(name="data_capacity", signature={"s1": satellite_domain.types["satellite"]})
    numeric_state_variables[data_capacity_function.untyped_representation].set_value(-5.3)
    numeric_state_variables[data_function.untyped_representation].set_value(-15.32)
    state_with_complete_predicates = State(predicates=complete_state_predicates, fluents=numeric_state_variables)
    assert satellite_action_precondition.is_applicable(state_with_complete_predicates)


def test_is_applicable_with_disjunctive_action_operator_does_not_fail(valid_previous_state: State):
    test_action_str = """  (take_image
   :parameters (?s - satellite ?d - direction ?i - instrument ?m - mode)
   :precondition (and (calibrated ?i)
                      (on_board ?i ?s)
                      (supports ?i ?m)
                      (power_on ?i)
                      (pointing ?s ?d)
                      (power_on ?i)
                      (or 
                      (and (>= (data_capacity ?s) (data ?d ?m)))
			          (and (>= (data_capacity ?s) 0))
               ))
   :effect (and (decrease (data_capacity ?s) (data ?d ?m)) (have_image ?d ?m)
		(increase (data-stored) (data ?d ?m)))
  )"""
    domain_parser = DomainParser(TEST_HARD_NUMERIC_DOMAIN)
    domain = domain_parser.parse_domain()
    action_tokens = PDDLTokenizer(pddl_str=test_action_str).parse()
    action = domain_parser.parse_action(action_tokens, domain.types, domain.functions, domain.predicates,
                                        domain.constants)
    grounded_precondition = GroundedPrecondition(action.preconditions, domain, action)
    test_parameter_map = {
        param: obj for param, obj in zip(action.signature.keys(), TEST_GROUNDED_ACTION_CALL)
    }
    grounded_precondition.ground_preconditions(test_parameter_map)
    try:
        grounded_precondition.is_applicable(valid_previous_state)

    except Exception:
        fail()


def test_is_applicable_returns_true_when_the_action_has_nested_universal_precondition_but_is_logically_the_same_as_the_original_action(
        miconic_nested_domain: Domain, miconic_nested_problem: Problem,
        miconic_stop_action_precondition: GroundedPrecondition, miconic_observation: Observation):
    miconic_stop_action_comp = miconic_observation.components[1]
    miconic_previous_state = miconic_stop_action_comp.previous_state
    test_parameters_map = {"?f": "f1"}
    miconic_stop_action_precondition.ground_preconditions(test_parameters_map)
    assert miconic_stop_action_precondition.is_applicable(miconic_previous_state)
