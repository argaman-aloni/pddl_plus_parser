"""Module test for the grounded operator class."""
from typing import List, Dict, Set

from pytest import fixture, fail

from pddl_plus_parser.lisp_parsers import DomainParser, PDDLTokenizer, ProblemParser
from pddl_plus_parser.models import Domain, Action, Operator, GroundedPredicate, PDDLFunction, State, Problem, \
    NumericalExpressionTree
from pddl_plus_parser.models.grounding_utils import ground_numeric_calculation_tree, ground_numeric_expressions
from tests.lisp_parsers_tests.consts import SPIDER_PROBLEM_PATH
from tests.models_tests.consts import TEST_HARD_NUMERIC_DOMAIN, TEST_NUMERIC_DOMAIN, SPIDER_DOMAIN_PATH, \
    NURIKABE_DOMAIN_PATH, NURIKABE_PROBLEM_PATH

TEST_LIFTED_SIGNATURE_ITEMS = ["?s", "?d", "?i", "?m"]
TEST_GROUNDED_ACTION_CALL = ["s1", "test_direction", "test_instrument", "test_mode"]

AGRICOLA_LIFTED_SIGNATURE_ITEMS = ["?w1", "?w2", "?wmax", "?r", "?i1", "?i2"]
AGRICOLA_GROUNDED_ACTION_CALL = ["noworker", "w1", "w2", "round1", "n1", "n2"]

SPIDER_START_DEALING_CALL = []
SPIDER_DEAL_CARD_CALL = ["card-d0-s1-v3", "card-d0-s0-v3", "deal-0", "card-d0-s3-v1", "pile-0"]
NURIKABE_START_PAINTING_CALL = ["pos-0-0", "g0", "n1", "n0"]
NURIKABE_MOVE_PAINTING_CALL = ["pos-2-0", "pos-3-0", "g1", "n1", "n0"]


@fixture()
def domain() -> Domain:
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
def spider_problem(spider_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SPIDER_PROBLEM_PATH, domain=spider_domain).parse_problem()


@fixture()
def nurikabe_problem(nurikabe_domain: Domain) -> Problem:
    return ProblemParser(problem_path=NURIKABE_PROBLEM_PATH, domain=nurikabe_domain).parse_problem()


@fixture()
def numeric_action(domain: Domain) -> Action:
    return domain.actions["take_image"]


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
def operator(domain: Domain, numeric_action: Action) -> Operator:
    return Operator(numeric_action, domain, TEST_GROUNDED_ACTION_CALL)


@fixture()
def agricola_operator(agricola_domain: Domain, agricola_numeric_action: Action) -> Operator:
    return Operator(agricola_numeric_action, agricola_domain, AGRICOLA_GROUNDED_ACTION_CALL)


@fixture()
def spider_start_dealing_operator(spider_domain: Domain, spider_unconditional_action: Action) -> Operator:
    return Operator(spider_unconditional_action, spider_domain, SPIDER_START_DEALING_CALL)


@fixture()
def spider_deal_card_operator(spider_domain: Domain, spider_conditional_action: Action) -> Operator:
    return Operator(spider_conditional_action, spider_domain, SPIDER_DEAL_CARD_CALL)


@fixture()
def nurikabe_start_painting_operator(nurikabe_domain: Domain, nurikabe_unconditional_action: Action) -> Operator:
    return Operator(nurikabe_unconditional_action, nurikabe_domain, NURIKABE_START_PAINTING_CALL)


@fixture()
def nurikabe_move_painting_operator(nurikabe_domain: Domain, nurikabe_conditional_action: Action,
                                    nurikabe_problem: Problem) -> Operator:
    return Operator(nurikabe_conditional_action, nurikabe_domain, NURIKABE_MOVE_PAINTING_CALL,
                    problem_objects=nurikabe_problem.objects)


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


def test_typed_action_call_returns_correct_string(operator: Operator):
    assert operator.typed_action_call == \
           "(take_image s1 - satellite test_direction - direction test_instrument - instrument test_mode - mode)"


def test_ground_numeric_function_when_domain_contains_constants_grounds_action_correctly(
        agricola_operator: Operator, agricola_numeric_action: Action, agricola_domain: Domain):
    test_grounded_call = ["w1", "w2", "noworker", "round1", "n1", "n2"]
    test_lifted_function = agricola_numeric_action.numeric_effects.pop()
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            AGRICOLA_LIFTED_SIGNATURE_ITEMS, test_grounded_call)
    }
    grounded_expression_tree = ground_numeric_calculation_tree(
        lifted_numeric_exp_tree=test_lifted_function, parameters_map=test_parameters_map, domain=agricola_domain)
    assert grounded_expression_tree.to_pddl() == "(increase (total-cost ) (group_worker_cost noworker))"


def test_ground_numeric_calculation_tree_extracts_correct_grounded_tree_data_from_lifted_calc_tree(
        operator: Operator, numeric_action: Action, domain: Domain):
    for precondition in numeric_action.preconditions:
        if isinstance(precondition, NumericalExpressionTree):
            test_lifted_expression_tree = precondition
            test_parameters_map = {
                lifted_param: grounded_object for lifted_param, grounded_object in zip(
                    TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
            }

            expression_tree = ground_numeric_calculation_tree(test_lifted_expression_tree, test_parameters_map, domain)

            root = expression_tree.root
            assert root.id == ">="
            assert root.children[0].id == "(data_capacity s1 - satellite)"
            assert root.children[1].id == "(data test_direction - direction test_mode - mode)"
            break


def test_ground_numeric_expressions_extracts_all_numeric_expressions(
        operator: Operator, numeric_action: Action, domain: Domain):
    test_lifted_expression_tree = numeric_action.numeric_effects
    test_parameters_map = {
        lifted_param: grounded_object for lifted_param, grounded_object in zip(
            TEST_LIFTED_SIGNATURE_ITEMS, TEST_GROUNDED_ACTION_CALL)
    }
    expression_tree_set = ground_numeric_expressions(test_lifted_expression_tree, test_parameters_map, domain)

    assert len(expression_tree_set) == 2


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
    test_operator = Operator(action, domain, TEST_GROUNDED_ACTION_CALL)
    try:
        test_operator.is_applicable(valid_previous_state)
    except Exception:
        fail()


def test_apply_with_conditional_effects_does_not_fail(
        spider_domain: Domain,
        spider_start_dealing_operator: Operator,
        spider_deal_card_operator: Operator,
        spider_problem: Problem):
    try:
        initial_state = State(spider_problem.initial_state_predicates, spider_problem.initial_state_fluents)
        second_state = spider_start_dealing_operator.apply(initial_state)
        third_state = spider_deal_card_operator.apply(second_state)
        assert third_state is not None

    except Exception:
        fail()


def test_apply_with_conditional_effects_outputs_conditional_effects_in_successive_state(
        spider_domain: Domain,
        spider_start_dealing_operator: Operator,
        spider_deal_card_operator: Operator,
        spider_problem: Problem):
    initial_state = State(spider_problem.initial_state_predicates, spider_problem.initial_state_fluents)
    second_state = spider_start_dealing_operator.apply(initial_state)
    third_state = spider_deal_card_operator.apply(second_state)
    state_predicates = set()
    for predicates in third_state.state_predicates.values():
        state_predicates.update(predicates)

    assert "(currently-updating-unmovable )" in [p.untyped_representation for p in state_predicates]
    assert "(make-unmovable card-d0-s3-v1)" in [p.untyped_representation for p in state_predicates]


def test_apply_with_action_with_universal_quantifier_applies_effects_on_all_objects_that_match_conditions(
        nurikabe_domain: Domain, nurikabe_move_painting_operator: Operator, nurikabe_problem: Problem):
    initial_state = State(nurikabe_problem.initial_state_predicates, nurikabe_problem.initial_state_fluents)
    serialized_initial_state = initial_state.serialize()
    assert "(blocked pos-2-0)" not in serialized_initial_state
    assert "(blocked pos-4-0)" not in serialized_initial_state
    new_state = nurikabe_move_painting_operator.apply(initial_state, allow_inapplicable_actions=True)
    serialized_state = new_state.serialize()
    assert "(available pos-2-0)" not in serialized_state
    assert "(available pos-4-0)" not in serialized_state
    assert "(part-of pos-2-0 g1)" not in serialized_state
    assert "(part-of pos-4-0 g1)" not in serialized_state
    assert "(blocked pos-2-0)" in serialized_state
    assert "(blocked pos-4-0)" in serialized_state
