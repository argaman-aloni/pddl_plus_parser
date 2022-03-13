"""Module test for the trajectory parser."""
from pytest import fixture, raises, fail

from lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from models import Domain, Problem
from tests.lisp_parsers_tests.consts import TEST_NUMERIC_DEPOT_DOMAIN, TEST_NUMERIC_DEPOT_PROBLEM, \
    TEST_NUMERIC_DEPOT_TRAJECTORY


@fixture()
def domain() -> Domain:
    domain_parser = DomainParser(TEST_NUMERIC_DEPOT_DOMAIN, partial_parsing=True)
    return domain_parser.parse_domain()

@fixture()
def problem(domain: Domain) -> Problem:
    return ProblemParser(problem_path=TEST_NUMERIC_DEPOT_PROBLEM, domain=domain).parse_problem()

@fixture()
def trajectory_parser(domain: Domain, problem: Problem) -> TrajectoryParser:
    return TrajectoryParser(domain, problem)

def test_parse_trajectory(trajectory_parser: TrajectoryParser):
    observation = trajectory_parser.parse_trajectory(TEST_NUMERIC_DEPOT_TRAJECTORY)
    assert len(observation.components) == 19
