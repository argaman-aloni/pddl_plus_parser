"""Module test for the numeric trajectory exporter functionality."""

import pytest
from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Domain, State, Problem
from pddl_plus_parser.multi_agent import MultiAgentTrajectoryExporter
from tests.multi_agent_tests.consts import COMBINED_DOMAIN_PATH, COMBINED_PROBLEM_PATH, WOODWORKING_PARSED_PLAN_PATH

WOODWORKING_AGENT_NAMES = ["glazer0", "grinder0", "highspeed-saw0", "immersion-varnisher0", "planer0", "saw0",
                           "spray-varnisher0"]


@fixture()
def combined_domain() -> Domain:
    domain_parser = DomainParser(COMBINED_DOMAIN_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def combined_problem(combined_domain: Domain) -> Problem:
    return ProblemParser(problem_path=COMBINED_PROBLEM_PATH, domain=combined_domain).parse_problem()


@fixture()
def multi_agent_trajectory_exporter(combined_domain: Domain) -> MultiAgentTrajectoryExporter:
    return MultiAgentTrajectoryExporter(domain=combined_domain)


def test_create_single_triplet_with_single_state_and_single_call_creates_next_state_correctly(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    test_action_call = "[(nop ),(do-grind grinder0 p0 smooth red varnished colourfragments),(nop ),(nop ),(nop ),(nop ),(nop )]"
    initial_state = State(predicates=combined_problem.initial_state_predicates,
                          fluents=combined_problem.initial_state_fluents)
    result_triplet = multi_agent_trajectory_exporter.create_multi_agent_triplet(initial_state, test_action_call)
    result_next_state = result_triplet.next_state
    grind_cost = initial_state.state_fluents["(grind-cost p0)"].value
    assert result_next_state.state_fluents["(total-cost )"].value == initial_state.state_fluents[
        "(total-cost )"].value + grind_cost


def test_create_single_triplet_with_single_state_and_single_call_with_two_executing_agents_sets_numeric_fluents_correctly(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    test_action_call = "[(nop ),(do-grind grinder0 p0 smooth red varnished colourfragments),(nop ),(nop ),(nop ),(nop ),(nop )]"
    two_agent_action_call = "[(nop ),(nop ),(nop ),(nop ),(do-plane planer0 p2 verysmooth natural varnished),(do-saw-medium saw0 b0 p1 pine rough s3 s2 s1),(nop )]"
    initial_state = State(predicates=combined_problem.initial_state_predicates,
                          fluents=combined_problem.initial_state_fluents)
    result_triplet = multi_agent_trajectory_exporter.create_multi_agent_triplet(initial_state, test_action_call)
    result_next_state = result_triplet.next_state

    result_triplet = multi_agent_trajectory_exporter.create_multi_agent_triplet(result_next_state,
                                                                                two_agent_action_call)
    total_cost_pre_action = 15
    assert result_triplet.next_state.state_fluents["(total-cost )"].value == total_cost_pre_action + 30 + \
           result_triplet.previous_state.state_fluents["(plane-cost p2)"].value


def test_create_single_triplet_with_single_state_and_single_call_with_two_executing_agents_creates_sets_predicates_correctly(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    test_action_call = "[(nop ),(do-grind grinder0 p0 smooth red varnished colourfragments),(nop ),(nop ),(nop ),(nop ),(nop )]"
    two_agent_action_call = "[(nop ),(nop ),(nop ),(nop ),(do-plane planer0 p2 verysmooth natural varnished)," \
                            "(do-saw-medium saw0 b0 p1 pine rough s3 s2 s1),(nop )]"
    initial_state = State(predicates=combined_problem.initial_state_predicates,
                          fluents=combined_problem.initial_state_fluents)
    result_triplet = multi_agent_trajectory_exporter.create_multi_agent_triplet(initial_state, test_action_call)
    result_next_state = result_triplet.next_state

    result_triplet = multi_agent_trajectory_exporter.create_multi_agent_triplet(result_next_state,
                                                                                two_agent_action_call)
    next_state_predicates = result_triplet.next_state.state_predicates
    unused_parts_predicates = [p.untyped_representation for p in next_state_predicates["(unused ?obj)"]]
    available_parts_predicates = [p.untyped_representation for p in next_state_predicates["(available ?obj)"]]
    surface_condition_parts_predicates = [p.untyped_representation for p in
                                          next_state_predicates["(surface-condition ?obj ?surface)"]]
    assert "(unused p1)" not in unused_parts_predicates
    assert "(available p1)" in available_parts_predicates
    assert "(surface-condition p2 smooth)" in surface_condition_parts_predicates


def test_parse_plan_can_parse_complete_plan_content_without_fail(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    try:
        multi_agent_trajectory_exporter.parse_plan(combined_problem, WOODWORKING_PARSED_PLAN_PATH)
    except Exception as e:
        pytest.fail(f"Failed to parse plan: {e}")


def test_parse_plan_can_parse_complete_plan_and_create_correct_length_trajectory(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    triplets = multi_agent_trajectory_exporter.parse_plan(combined_problem, WOODWORKING_PARSED_PLAN_PATH)
    assert len(triplets) == 4


def test_export_returns_readable_list_of_strings_representing_the_trajectory(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    triplets = multi_agent_trajectory_exporter.parse_plan(combined_problem, WOODWORKING_PARSED_PLAN_PATH)
    trajectory_lines = multi_agent_trajectory_exporter.export(triplets)
    for line in trajectory_lines:
        print(line)
