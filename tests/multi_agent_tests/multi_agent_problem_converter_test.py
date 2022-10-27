"""Module test for the multi-agent to single agent problem convertion."""
from pytest import fixture

from pddl_plus_parser.multi_agent import MultiAgentProblemsConverter
from tests.multi_agent_tests.consts import MULTI_AGENT_DATA_DIRECTORY, COMBINED_DOMAIN_PATH, \
    ANOTHER_MULTI_AGENT_DATA_DIRECTORY, LOGISTICS_MA_DOMAIN_PATH


@fixture()
def problem_converter() -> MultiAgentProblemsConverter:
    return MultiAgentProblemsConverter(MULTI_AGENT_DATA_DIRECTORY, problem_file_prefix="problem")


@fixture()
def logistics_problem_converter() -> MultiAgentProblemsConverter:
    return MultiAgentProblemsConverter(ANOTHER_MULTI_AGENT_DATA_DIRECTORY, problem_file_prefix="problem")


def test_combine_problems_returns_problem_with_correct_name(problem_converter: MultiAgentProblemsConverter):
    combined_problem = problem_converter.combine_problems(COMBINED_DOMAIN_PATH)
    assert combined_problem.name == "wood-prob"


def test_combine_problems_returns_problem_with_all_private_and_public_objects(
        problem_converter: MultiAgentProblemsConverter):
    combined_problem = problem_converter.combine_problems(COMBINED_DOMAIN_PATH)
    assert "highspeed-saw0" in combined_problem.objects


def test__combine_problems_returns_problem_with_initial_state_with_private_objects(
        problem_converter: MultiAgentProblemsConverter):
    combined_problem = problem_converter.combine_problems(COMBINED_DOMAIN_PATH)
    assert "(empty ?agent)" in combined_problem.initial_state_predicates
    empty_predicates = combined_problem.initial_state_predicates["(empty ?agent)"]
    assert "(empty highspeed-saw0)" in [p.untyped_representation for p in empty_predicates]


def test_combine_problems_returns_problem_with_initial_state_with_unique_predicates(
        logistics_problem_converter: MultiAgentProblemsConverter):
    combined_problem = logistics_problem_converter.combine_problems(LOGISTICS_MA_DOMAIN_PATH)
    all_initial_states_predicates = []
    for predicates in combined_problem.initial_state_predicates.values():
        all_initial_states_predicates.extend([p.untyped_representation for p in predicates])

    assert len(set(all_initial_states_predicates)) == len(all_initial_states_predicates)
