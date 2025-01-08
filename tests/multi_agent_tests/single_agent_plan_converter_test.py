"""Module test for the single agent plan converter."""
import pytest
from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Domain, Problem
from pddl_plus_parser.multi_agent import PlanConverter
from tests.multi_agent_tests.consts import SOKOBAN_DOMAIN_FILE_PATH, SOKOBAN_UNPARSED_PLAN_PATH, \
    WOODWORKING_UNPARSED_PLAN_PATH, WOODWORKING_AGENT_NAMES, COMBINED_PROBLEM_PATH, \
    SOKOBAN_PROBLEM_PATH, COMBINED_DOMAIN_PATH, SOKOBAN_PROBLEM_WITH_INTERACTING_ACTIONS_PATH, \
    SOKOBAN_UNPARSED_PLAN_WITH_INTERACTING_ACTIONS_PATH, DEPOT1_MA_PROBLEM_PATH, \
    DEPOT1_MA_DOMAIN_PATH, DEPOT1_MA_SOLUTION_PATH

SOKOBAN_AGENT_NAMES = ["player-01", "player-02"]


@fixture()
def sokoban_domain() -> Domain:
    domain_parser = DomainParser(SOKOBAN_DOMAIN_FILE_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def sokoban_plan_converter(sokoban_domain: Domain) -> PlanConverter:
    return PlanConverter(sokoban_domain)


@fixture()
def woodworking_domain() -> Domain:
    domain_parser = DomainParser(COMBINED_DOMAIN_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def woodworking_problem(woodworking_domain: Domain) -> Problem:
    return ProblemParser(problem_path=COMBINED_PROBLEM_PATH, domain=woodworking_domain).parse_problem()


@fixture()
def sokoban_problem(sokoban_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SOKOBAN_PROBLEM_PATH, domain=sokoban_domain).parse_problem()


@fixture()
def sokoban_problem_with_interacting_actions(sokoban_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SOKOBAN_PROBLEM_WITH_INTERACTING_ACTIONS_PATH,
                         domain=sokoban_domain).parse_problem()


@fixture()
def woodworking_plan_converter(woodworking_domain: Domain) -> PlanConverter:
    return PlanConverter(woodworking_domain)


@fixture()
def depots_domain() -> Domain:
    domain_parser = DomainParser(DEPOT1_MA_DOMAIN_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def depots_plan_converter(depots_domain: Domain) -> PlanConverter:
    return PlanConverter(depots_domain)


@fixture()
def depots_problem_with_conflicting_joint_actions(depots_domain: Domain) -> Problem:
    return ProblemParser(problem_path=DEPOT1_MA_PROBLEM_PATH,
                         domain=depots_domain).parse_problem()


def test_convert_plan_does_not_remove_actions_from_original_plan(sokoban_plan_converter: PlanConverter,
                                                                 sokoban_problem: Problem):
    joint_actions = sokoban_plan_converter.convert_plan(sokoban_problem, SOKOBAN_UNPARSED_PLAN_PATH,
                                                        agent_names=SOKOBAN_AGENT_NAMES)
    assert sum([action.action_count for action in joint_actions]) == 28


def test_convert_plan_reduce_plan_length(sokoban_plan_converter: PlanConverter, sokoban_problem: Problem):
    joint_actions = sokoban_plan_converter.convert_plan(sokoban_problem, SOKOBAN_UNPARSED_PLAN_PATH,
                                                        agent_names=SOKOBAN_AGENT_NAMES)
    assert len(joint_actions) < 28


def test_convert_plan_does_not_have_joint_actions_with_same_agent(sokoban_plan_converter: PlanConverter,
                                                                  sokoban_problem: Problem):
    joint_actions = sokoban_plan_converter.convert_plan(
        sokoban_problem, SOKOBAN_UNPARSED_PLAN_PATH, agent_names=SOKOBAN_AGENT_NAMES)
    for joint_action in joint_actions:
        assert len([param for param in joint_action.joint_parameters if param == SOKOBAN_AGENT_NAMES[0]]) <= 1
        assert len([param for param in joint_action.joint_parameters if param == SOKOBAN_AGENT_NAMES[1]]) <= 1


def test_convert_plan_allows_fully_interacting_actions_to_be_executed_concurrently(
        sokoban_plan_converter: PlanConverter, sokoban_problem_with_interacting_actions: Problem):
    try:
        joint_actions = sokoban_plan_converter.convert_plan(
            sokoban_problem_with_interacting_actions, SOKOBAN_UNPARSED_PLAN_WITH_INTERACTING_ACTIONS_PATH,
            agent_names=SOKOBAN_AGENT_NAMES, should_validate_concurrency_constraint=False)
        for joint_action in joint_actions:
            print([str(action) for action in joint_action.actions])
    except Exception:
        pytest.fail("Exception raised when converting plan with fully interacting actions")


def test_convert_plan_does_not_remove_actions_from_original_plan_when_domain_contains_constants(
        woodworking_plan_converter: PlanConverter, woodworking_problem: Problem):
    joint_actions = woodworking_plan_converter.convert_plan(woodworking_problem, WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)
    assert sum([action.action_count for action in joint_actions]) == 6


def test_convert_plan_reduce_plan_length_when_domain_contains_constants(
        woodworking_plan_converter: PlanConverter, woodworking_problem: Problem):
    joint_actions = woodworking_plan_converter.convert_plan(woodworking_problem, WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)
    assert len(joint_actions) < 6


def test_convert_plan_does_not_have_joint_actions_with_same_agent_when_domain_contains_constants(
        woodworking_plan_converter: PlanConverter, woodworking_problem: Problem):
    joint_actions = woodworking_plan_converter.convert_plan(woodworking_problem, WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)
    for joint_action in joint_actions:
        for agent_name in WOODWORKING_AGENT_NAMES:
            assert len([param for param in joint_action.joint_parameters if param == agent_name]) <= 1


def test_convert_plan_produces_readable_plan(woodworking_plan_converter: PlanConverter, woodworking_problem: Problem):
    joint_actions = woodworking_plan_converter.convert_plan(woodworking_problem, WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)

    print()
    for joint_action in joint_actions:
        print(joint_action)


def test_convert_plan_when_removing_concurrency_constraint_creates_shorter_plan_than_if_we_do_not(
        woodworking_plan_converter: PlanConverter, woodworking_problem: Problem):
    short_joint_actions = woodworking_plan_converter.convert_plan(woodworking_problem,
                                                                  WOODWORKING_UNPARSED_PLAN_PATH,
                                                                  agent_names=WOODWORKING_AGENT_NAMES,
                                                                  should_validate_concurrency_constraint=False)
    longer_joint_actions = woodworking_plan_converter.convert_plan(woodworking_problem,
                                                                   WOODWORKING_UNPARSED_PLAN_PATH,
                                                                   agent_names=WOODWORKING_AGENT_NAMES)
    assert len(short_joint_actions) <= len(longer_joint_actions)

    print()
    for joint_action in short_joint_actions:
        print(joint_action)


def test_convert_plan_when_some_actions_contain_effects_that_delete_preconditions_do_not_combine_to_the_same_joint_actions(
        depots_plan_converter: PlanConverter, depots_problem_with_conflicting_joint_actions: Problem):
    depots_agents = ["depot0","depot1","depot2","depot3","distributor0","distributor1","distributor2","distributor3","driver0","driver1","driver2","driver3"]
    short_joint_actions = depots_plan_converter.convert_plan(depots_problem_with_conflicting_joint_actions,
                                                                  DEPOT1_MA_SOLUTION_PATH,
                                                                  agent_names=depots_agents)
    for joint_action in short_joint_actions:
        assert "[(nop ),(nop ),(unload depot2 hoist2 crate3 truck0),(nop ),(nop ),(nop ),(nop ),(nop ),(drive driver0 truck0 depot2 depot0),(nop ),(nop ),(nop )]" != str(joint_action)