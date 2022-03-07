"""Module test for the numeric trajectory exporter functionality."""
import os
from collections import defaultdict
from pathlib import Path
from typing import List

from pytest import fixture, raises, fail

from exporters.numeric_trajectory_exporter import TrajectoryExporter
from lisp_parsers import DomainParser, ProblemParser
from models import Domain, Action, Operator, GroundedPredicate, PDDLFunction, State, Problem

CWD = os.getcwd()
TEST_DISCRETE_DOMAIN_PATH = Path(CWD, "elevators_domain.pddl")
TEST_DISCRETE_PROBLEM_PATH = Path(CWD, "elevators_p03.pddl")
TEST_DISCRETE_PLAN_PATH = Path(CWD, "elevators_p03_plan.solution")


@fixture()
def discrete_domain() -> Domain:
    domain_parser = DomainParser(TEST_DISCRETE_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def discrete_problem_parser(discrete_domain: Domain) -> ProblemParser:
    return ProblemParser(problem_path=TEST_DISCRETE_PROBLEM_PATH, domain=discrete_domain)

@fixture()
def discrete_problem(discrete_problem_parser) -> Problem:
    return discrete_problem_parser.parse_problem()


@fixture()
def discrete_trajectory_exporter(discrete_domain: Domain) -> TrajectoryExporter:
    return TrajectoryExporter(domain=discrete_domain)


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
        discrete_trajectory_exporter: TrajectoryExporter, discrete_problem_parser: ProblemParser):
    test_simple_state_components = [["lift-at", "slow2-0", "n17"], ["above", "n16", "n17"],
                                    ["reachable-floor", "slow2-0", "n16"]]
    test_action_call = "(move-down-slow slow2-0 n17 n16)"
    state = create_state_from_predicate_components(test_simple_state_components, discrete_problem_parser)
    print()
    print(state.serialize())
    result_triplet = discrete_trajectory_exporter.create_single_triplet(state, test_action_call)
    print(result_triplet)

def test_export(discrete_trajectory_exporter: TrajectoryExporter, discrete_problem: Problem):
    triplets = discrete_trajectory_exporter.parse_plan(discrete_problem, TEST_DISCRETE_PLAN_PATH)
    print(discrete_trajectory_exporter.export(triplets))
