from pytest import fixture

from pddl_plus_parser.lisp_parsers import ProblemParser, DomainParser
from pddl_plus_parser.models import Domain, Problem, State
from tests.models_tests.consts import TEST_NUMERIC_DOMAIN, TEST_NUMERIC_PROBLEM, SPIDER_DOMAIN_PATH, SPIDER_PROBLEM_PATH


@fixture()
def agricola_domain() -> Domain:
    domain_parser = DomainParser(TEST_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def agricola_problem(agricola_domain: Domain) -> Problem:
    return ProblemParser(problem_path=TEST_NUMERIC_PROBLEM, domain=agricola_domain).parse_problem()


@fixture()
def spider_domain() -> Domain:
    domain_parser = DomainParser(SPIDER_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def spider_problem(spider_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SPIDER_PROBLEM_PATH, domain=spider_domain).parse_problem()


@fixture()
def spider_first_state(spider_problem: Problem) -> State:
    return State(predicates=spider_problem.initial_state_predicates, fluents=spider_problem.initial_state_fluents)


def test_states_are_equal_when_states_contain_only_predicates(spider_problem: Problem):
    state1 = State(predicates=spider_problem.initial_state_predicates, fluents={})
    state2 = State(predicates=spider_problem.initial_state_predicates, fluents={})
    assert state1 == state2


def test_states_are_not_equal_when_states_contain_only_predicates_and_one_state_is_missing_predicate(
        spider_problem: Problem):
    state1 = State(predicates=spider_problem.initial_state_predicates, fluents={})
    state2 = state1.copy()
    state1.state_predicates["(clear ?c)"].pop()
    assert not state1 == state2


def test_states_are_equal_when_states_contain_predicates_and_numeric_value_and_all_are_equal(
        agricola_problem: Problem):
    state1 = State(predicates=agricola_problem.initial_state_predicates, fluents=agricola_problem.initial_state_fluents)
    state2 = state1.copy()
    assert state1 == state2


def test_states_are_not_equal_when_states_contain_predicates_and_numeric_and_one_predicate_is_missing_from_one_state(
        agricola_problem: Problem):
    state1 = State(predicates=agricola_problem.initial_state_predicates, fluents=agricola_problem.initial_state_fluents)
    state2 = state1.copy()
    state1.state_predicates["(next_round ?r1 ?r2)"].pop()
    assert not state1 == state2


def test_states_are_not_equal_when_states_contain_predicates_and_numeric_and_one_function_is_removed(
        agricola_problem: Problem):
    state1 = State(predicates=agricola_problem.initial_state_predicates, fluents=agricola_problem.initial_state_fluents)
    state2 = state1.copy()
    del state1.state_fluents["(group_worker_cost worker2)"]
    assert not state1 == state2


def test_states_are_not_equal_when_states_contain_predicates_and_numeric_and_one_function_value_is_changed(
        agricola_problem: Problem):
    state1 = State(predicates=agricola_problem.initial_state_predicates, fluents=agricola_problem.initial_state_fluents)
    state2 = state1.copy()
    state1.state_fluents["(group_worker_cost worker2)"].set_value(2)
    assert not state1 == state2


def test_convert_fluents_to_numeric_conditions_converts_the_state_fluents_with_their_values_correctly(
        agricola_problem: Problem):
    state1 = State(predicates=agricola_problem.initial_state_predicates, fluents=agricola_problem.initial_state_fluents)
    num_fluents = len(state1.state_fluents)
    numerical_fluents = state1.convert_fluents_to_numeric_conditions()
    assert len(numerical_fluents) == num_fluents


def test_get_state_objects_extract_all_objects_from_state(spider_first_state: State):
    objects = spider_first_state.get_state_objects()
    assert len(objects) == 31
    assert len([obj for obj in objects.keys() if obj.startswith("card")]) == 24
    assert len([obj for obj in objects.keys() if obj.startswith("pile")]) == 4
    assert len([obj for obj in objects.keys() if obj.startswith("deal")]) == 3
