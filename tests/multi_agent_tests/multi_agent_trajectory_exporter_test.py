"""Module test for the numeric trajectory exporter functionality."""

import pytest
from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Domain, State, Problem
from pddl_plus_parser.multi_agent import MultiAgentTrajectoryExporter
from tests.multi_agent_tests.consts import COMBINED_DOMAIN_PATH, COMBINED_PROBLEM_PATH, WOODWORKING_PARSED_PLAN_PATH, \
    WOODWORKING_SHORT_PARSED_PLAN_PATH, DEPOT_MA_DOMAIN_PATH, DEPOT_MA_PROBLEM_PATH, DEPOT_MA_SOLUTION_PATH, \
    DEPOT_MA_CONCURRENT_PROBLEM_PATH


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


@fixture()
def ma_depot_domain() -> Domain:
    return DomainParser(DEPOT_MA_DOMAIN_PATH, partial_parsing=False).parse_domain()


@fixture()
def ma_depot_problem(ma_depot_domain: Domain) -> Problem:
    return ProblemParser(problem_path=DEPOT_MA_PROBLEM_PATH, domain=ma_depot_domain).parse_problem()


@fixture()
def ma_depot_problem2(ma_depot_domain: Domain) -> Problem:
    return ProblemParser(problem_path=DEPOT_MA_CONCURRENT_PROBLEM_PATH, domain=ma_depot_domain).parse_problem()


@fixture()
def multi_agent_depots_trajectory_exporter(ma_depot_domain: Domain) -> MultiAgentTrajectoryExporter:
    return MultiAgentTrajectoryExporter(domain=ma_depot_domain)


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


def test_export_with_interacting_plan_returns_readable_list_of_strings_representing_the_trajectory(
        multi_agent_trajectory_exporter: MultiAgentTrajectoryExporter, combined_problem: Problem):
    triplets = multi_agent_trajectory_exporter.parse_plan(combined_problem, WOODWORKING_SHORT_PARSED_PLAN_PATH)
    trajectory_lines = multi_agent_trajectory_exporter.export(triplets)
    for line in trajectory_lines:
        print(line)


def test_create_trajectory_triplet_applies_action_on_state_and_removes_delete_effects_from_the_next_state(
        multi_agent_depots_trajectory_exporter: MultiAgentTrajectoryExporter, ma_depot_problem: Problem):
    triplets = multi_agent_depots_trajectory_exporter.parse_plan(ma_depot_problem, DEPOT_MA_SOLUTION_PATH)
    trajectory_lines = multi_agent_depots_trajectory_exporter.export(triplets)
    print()
    for line in trajectory_lines:
        print(line)


def test_create_trajectory_triplet_applies_action_on_state_and_removes_delete_effects_from_the_next_state_when_two_actions_are_executed_concurrently(
        multi_agent_depots_trajectory_exporter: MultiAgentTrajectoryExporter, ma_depot_problem2: Problem):
    previous_state = State(predicates=ma_depot_problem2.initial_state_predicates,
                           fluents=ma_depot_problem2.initial_state_fluents)
    action_call = "[(nop ),(nop ),(lift hoist2 crate1 pallet2 distributor1),(nop ),(nop ),(nop ),(drive truck1 distributor0 depot0),(nop ),(nop )]"
    triplet = multi_agent_depots_trajectory_exporter.create_multi_agent_triplet(previous_state=previous_state,
                                                                                action_call=action_call)
    print(triplet)
    at_item_predicates = triplet.next_state.state_predicates["(at ?x ?y)"]
    at_predicates_str = [p.untyped_representation for p in at_item_predicates]
    assert "(at truck1 distributor0)" not in at_predicates_str
