"""Module test for the trajectory parser."""
from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from pddl_plus_parser.models import Domain, Problem
from tests.lisp_parsers_tests.consts import TEST_NUMERIC_DEPOT_DOMAIN, TEST_NUMERIC_DEPOT_PROBLEM, \
    TEST_NUMERIC_DEPOT_TRAJECTORY, FARMLAND_NUMERIC_DOMAIN, FARMLAND_NUMERIC_PROBLEM, FARMLAND_NUMERIC_TRAJECTORY


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


@fixture()
def farmland_domain() -> Domain:
    domain_parser = DomainParser(FARMLAND_NUMERIC_DOMAIN, partial_parsing=True)
    return domain_parser.parse_domain()

@fixture()
def farmland_problem(farmland_domain: Domain) -> Problem:
    return ProblemParser(problem_path=FARMLAND_NUMERIC_PROBLEM, domain=farmland_domain).parse_problem()

@fixture()
def farmland_trajectory_parser(farmland_domain: Domain, farmland_problem: Problem) -> TrajectoryParser:
    return TrajectoryParser(farmland_domain, farmland_problem)


def test_parse_trajectory(trajectory_parser: TrajectoryParser):
    observation = trajectory_parser.parse_trajectory(TEST_NUMERIC_DEPOT_TRAJECTORY)
    assert len(observation.components) == 19


def test_parse_farmland_trajectory(farmland_trajectory_parser: TrajectoryParser):
    observation = farmland_trajectory_parser.parse_trajectory(FARMLAND_NUMERIC_TRAJECTORY)
    assert len(observation.components) == 12