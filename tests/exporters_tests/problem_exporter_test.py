"""Module test for the problem exporter."""
from pathlib import Path

from pytest import fixture

from pddl_plus_parser.exporters import ProblemExporter
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Problem, Domain
from .consts import TEST_MINECRAFT_DOMAIN_PATH, TEST_MINECRAFT_PROBLEM_PATH


@fixture
def problem_exporter() -> ProblemExporter:
    """Creates a new instance of the ProblemExporter class."""
    return ProblemExporter()


@fixture()
def minecraft_domain() -> Domain:
    domain_parser = DomainParser(TEST_MINECRAFT_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def minecraft_problem(minecraft_domain: Domain) -> Problem:
    return ProblemParser(problem_path=TEST_MINECRAFT_PROBLEM_PATH, domain=minecraft_domain).parse_problem()


def test_export_problem_when_defining_a_problem_with_an_initial_state_and_a_goal_exports_the_problem_and_the_content_is_the_same_as_the_original_problem(
        problem_exporter: ProblemExporter, minecraft_problem: Problem, minecraft_domain: Domain):
    """Test that the problem is exported correctly."""
    problem_path = Path("problem.pddl")
    problem_exporter.export_problem(minecraft_problem, problem_path)
    generated_problem = ProblemParser(problem_path=problem_path, domain=minecraft_domain).parse_problem()
    assert generated_problem.initial_state_predicates == minecraft_problem.initial_state_predicates
    assert generated_problem.goal_state_predicates == minecraft_problem.goal_state_predicates
    assert generated_problem.initial_state_fluents == minecraft_problem.initial_state_fluents
    assert generated_problem.objects == minecraft_problem.objects
    problem_path.unlink()


def test_export_problem_when_defining_a_problem_with_empty_goal_state_returns_a_new_problem_with_an_empty_goal_state_as_well(
        problem_exporter: ProblemExporter, minecraft_problem: Problem, minecraft_domain: Domain):
    """Test that the problem is exported correctly."""
    problem_path = Path("problem.pddl")
    minecraft_problem.goal_state_predicates = []
    minecraft_problem.goal_state_fluents = set()
    problem_exporter.export_problem(minecraft_problem, problem_path)
    generated_problem = ProblemParser(problem_path=problem_path, domain=minecraft_domain).parse_problem()
    assert generated_problem.initial_state_predicates == minecraft_problem.initial_state_predicates
    assert generated_problem.initial_state_fluents == minecraft_problem.initial_state_fluents
    assert len(generated_problem.goal_state_predicates) == 0
    assert len(generated_problem.goal_state_fluents) == 0
    assert generated_problem.objects == minecraft_problem.objects
    problem_path.unlink()
