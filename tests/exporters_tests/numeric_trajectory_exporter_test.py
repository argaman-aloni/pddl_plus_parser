"""Module test for the numeric trajectory exporter functionality."""
from collections import defaultdict
from typing import List

import pytest
from pytest import fixture

from pddl_plus_parser.exporters import TrajectoryExporter
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Domain, State, Problem
from .consts import TEST_DISCRETE_DOMAIN_PATH, TEST_DISCRETE_PROBLEM_PATH, TEST_DISCRETE_PLAN_PATH, \
    TEST_NUMERIC_DOMAIN_PATH, TEST_NUMERIC_PROBLEM_PATH, TEST_NUMERIC_PLAN_PATH, TEST_FAULTY_NUMERIC_PLAN_PATH, \
    TEST_DISCRETE_TRAJECTORY_FILE_PATH, TEST_NUMERIC_TRAJECTORY_FILE_PATH, TEST_CONDITIONAL_DOMAIN_PATH, \
    TEST_CONDITIONAL_PROBLEM_PATH, TEST_CONDITIONAL_PLAN_PATH, TEST_MINECRAFT_DOMAIN_PATH, TEST_MINECRAFT_PROBLEM_PATH, \
    TEST_MINECRAFT_PLAN_PATH, TEST_MICONIC_DOMAIN_PATH, TEST_MICONIC_PROBLEM_PATH, TEST_MICONIC_PLAN_PATH


@fixture()
def discrete_domain() -> Domain:
    domain_parser = DomainParser(TEST_DISCRETE_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def numeric_domain() -> Domain:
    domain_parser = DomainParser(TEST_NUMERIC_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def conditional_domain() -> Domain:
    domain_parser = DomainParser(TEST_CONDITIONAL_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def minecraft_domain() -> Domain:
    domain_parser = DomainParser(TEST_MINECRAFT_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def miconic_domain() -> Domain:
    domain_parser = DomainParser(TEST_MICONIC_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def discrete_problem_parser(discrete_domain: Domain) -> ProblemParser:
    return ProblemParser(problem_path=TEST_DISCRETE_PROBLEM_PATH, domain=discrete_domain)


@fixture()
def numeric_problem_parser(numeric_domain: Domain) -> ProblemParser:
    return ProblemParser(problem_path=TEST_NUMERIC_PROBLEM_PATH, domain=numeric_domain)


@fixture()
def conditional_problem_parser(conditional_domain: Domain) -> ProblemParser:
    return ProblemParser(problem_path=TEST_CONDITIONAL_PROBLEM_PATH, domain=conditional_domain)


@fixture()
def discrete_problem(discrete_problem_parser: ProblemParser) -> Problem:
    return discrete_problem_parser.parse_problem()


@fixture()
def numeric_problem(numeric_problem_parser: ProblemParser) -> Problem:
    return numeric_problem_parser.parse_problem()


@fixture()
def conditional_problem(conditional_problem_parser: ProblemParser) -> Problem:
    return conditional_problem_parser.parse_problem()


@fixture()
def minecraft_problem(minecraft_domain: Domain) -> Problem:
    return ProblemParser(problem_path=TEST_MINECRAFT_PROBLEM_PATH, domain=minecraft_domain).parse_problem()


@fixture()
def miconic_problem(miconic_domain: Domain) -> Problem:
    return ProblemParser(problem_path=TEST_MICONIC_PROBLEM_PATH, domain=miconic_domain).parse_problem()


@fixture()
def discrete_trajectory_exporter(discrete_domain: Domain) -> TrajectoryExporter:
    return TrajectoryExporter(domain=discrete_domain)


@fixture()
def numeric_trajectory_exporter(numeric_domain: Domain) -> TrajectoryExporter:
    return TrajectoryExporter(domain=numeric_domain)


@fixture()
def conditional_trajectory_exporter(conditional_domain: Domain) -> TrajectoryExporter:
    return TrajectoryExporter(domain=conditional_domain)


@fixture()
def minecraft_trajectory_exporter(minecraft_domain: Domain) -> TrajectoryExporter:
    return TrajectoryExporter(domain=minecraft_domain)


@fixture()
def miconic_trajectory_exporter(miconic_domain: Domain) -> TrajectoryExporter:
    return TrajectoryExporter(domain=miconic_domain)


def create_state_from_predicate_components(
        components: List[List[str]], problem_parser: ProblemParser) -> State:
    problem_parser.parse_problem()
    problem_parser.problem.initial_state_predicates = defaultdict(set)
    problem_parser.problem.initial_state_fluents = {}
    problem_parser.parse_initial_state(components)
    problem = problem_parser.problem
    initial_state_predicates = problem.initial_state_predicates
    initial_state_numeric_fluents = problem.initial_state_fluents
    return State(predicates=initial_state_predicates, fluents=initial_state_numeric_fluents)


def test_create_single_triplet_with_single_state_and_single_call_creates_next_state_correctly(
        discrete_trajectory_exporter: TrajectoryExporter, discrete_problem_parser: ProblemParser,
        discrete_problem: Problem):
    test_simple_state_components = [["lift-at", "slow2-0", "n17"], ["above", "n16", "n17"],
                                    ["reachable-floor", "slow2-0", "n16"]]
    test_action_call = "(move-down-slow slow2-0 n17 n16)"
    state = create_state_from_predicate_components(test_simple_state_components, discrete_problem_parser)
    result_triplet = discrete_trajectory_exporter.create_single_triplet(
        state, test_action_call, discrete_problem.objects)
    result_next_state = result_triplet.next_state
    lift_at_predicate = result_next_state.state_predicates["(lift-at ?lift ?floor)"]
    untyped_predicates = [p.untyped_representation for p in lift_at_predicate]
    assert "(lift-at slow2-0 n16)" in untyped_predicates
    assert "(lift-at slow2-0 n17)" not in untyped_predicates


def test_create_single_triplet_with_complete_initial_state_removes_correct_predicates_and_adds_correct_predicates(
        discrete_trajectory_exporter: TrajectoryExporter, discrete_problem: Problem):
    state = State(predicates=discrete_problem.initial_state_predicates, fluents={})
    test_action_call = "(move-down-slow slow2-0 n17 n16)"
    result_triplet = discrete_trajectory_exporter.create_single_triplet(state, test_action_call,
                                                                        discrete_problem.objects)
    lift_at_predicate = result_triplet.next_state.state_predicates["(lift-at ?lift ?floor)"]
    untyped_predicates = [p.untyped_representation for p in lift_at_predicate]
    assert "(lift-at slow2-0 n16)" in untyped_predicates
    assert "(lift-at slow2-0 n17)" not in untyped_predicates


def test_create_single_triplet_with_complete_numeric_initial_state_removes_correct_predicates_and_adds_correct_predicates(
        numeric_trajectory_exporter: TrajectoryExporter, numeric_problem: Problem):
    state = State(predicates=numeric_problem.initial_state_predicates, fluents=numeric_problem.initial_state_fluents)
    test_action_call = "(DRIVE TRUCK0 DEPOT0 DISTRIBUTOR0)"
    result_triplet = numeric_trajectory_exporter.create_single_triplet(state, test_action_call, numeric_problem.objects)
    test_next_state = result_triplet.next_state
    fuel_level_fluent = test_next_state.state_fluents["(fuel-cost )"]
    assert fuel_level_fluent.value == 10


def test_export_discrete_trajectory(discrete_trajectory_exporter: TrajectoryExporter, discrete_problem: Problem):
    triplets = discrete_trajectory_exporter.parse_plan(discrete_problem, TEST_DISCRETE_PLAN_PATH)
    exportable_triplets = discrete_trajectory_exporter.export(triplets)
    with open(TEST_DISCRETE_TRAJECTORY_FILE_PATH, "wt") as trajectory_file:
        trajectory_file.writelines(exportable_triplets)


def test_export_numeric_trajectory(numeric_trajectory_exporter: TrajectoryExporter, numeric_problem: Problem):
    triplets = numeric_trajectory_exporter.parse_plan(numeric_problem, TEST_NUMERIC_PLAN_PATH)
    exportable_triplets = numeric_trajectory_exporter.export(triplets)
    with open(TEST_NUMERIC_TRAJECTORY_FILE_PATH, "wt") as trajectory_file:
        trajectory_file.writelines(exportable_triplets)


def test_export_numeric_trajectory_with_faulty_action_creates_trajectory_with_action_but_with_unchanged_states(
        numeric_trajectory_exporter: TrajectoryExporter, numeric_problem: Problem):
    triplets = numeric_trajectory_exporter.parse_plan(numeric_problem, TEST_FAULTY_NUMERIC_PLAN_PATH)
    exportable_triplets = numeric_trajectory_exporter.export(triplets)
    pre_state = exportable_triplets[6]
    post_state = exportable_triplets[8]
    assert pre_state == post_state
    assert "(lift hoist1 crate3 pallet1 distributor0)" in exportable_triplets[5]


def test_export_numeric_trajectory_with_faulty_action_creates_but_does_not_duplicate_the_initial_state_multiple_times(
        minecraft_trajectory_exporter: TrajectoryExporter, minecraft_problem: Problem):
    triplets = minecraft_trajectory_exporter.parse_plan(minecraft_problem, TEST_MINECRAFT_PLAN_PATH)
    exportable_triplets = minecraft_trajectory_exporter.export(triplets)
    assert len([triplet for triplet in exportable_triplets if triplet.startswith("((:init")]) == 1


def test_export_trajectory_with_conditional_effects(
        conditional_trajectory_exporter: TrajectoryExporter, conditional_problem: Problem):
    triplets = conditional_trajectory_exporter.parse_plan(conditional_problem, TEST_CONDITIONAL_PLAN_PATH)
    try:
        exportable_triplets = conditional_trajectory_exporter.export(triplets)
        for triplet in exportable_triplets:
            print(triplet)

    except Exception as e:
        pytest.fail("Exporting a trajectory with conditional effects failed with the following error: " + str(e))


def test_export_trajectory_with_universal_effects_applies_universal_effects_only_when_all_the_conditions_apply(
        miconic_trajectory_exporter: TrajectoryExporter, miconic_problem: Problem):
    triplets = miconic_trajectory_exporter.parse_plan(miconic_problem, TEST_MICONIC_PLAN_PATH)
    print()
    for triplet in triplets:
        if triplet.operator.name == "stop" and str(triplet.operator) == "(stop f12)":
            op = triplet.operator
            print(triplet.previous_state.serialize())
            print(str(triplet.operator))
            print(triplet.next_state.serialize())
            print()
