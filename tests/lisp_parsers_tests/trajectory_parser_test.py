"""Module test for the trajectory parser."""

import pytest
from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from pddl_plus_parser.models import Domain, Problem, MultiAgentObservation
from tests.lisp_parsers_tests.consts import (
    TEST_NUMERIC_DEPOT_DOMAIN,
    TEST_NUMERIC_DEPOT_PROBLEM,
    TEST_NUMERIC_DEPOT_TRAJECTORY,
    FARMLAND_NUMERIC_DOMAIN,
    FARMLAND_NUMERIC_PROBLEM,
    FARMLAND_NUMERIC_TRAJECTORY,
    WOODWORKING_COMBINED_DOMAIN_PATH,
    WOODWORKING_COMBINED_PROBLEM_PATH,
    WOODWORKING_COMBINED_TRAJECTORY_PATH,
    DEPOT_MA_PROBLEM_PATH,
    DEPOT_MA_DOMAIN_PATH,
    DEPOT_MA_TRAJECTORY_PATH,
    LOGISTICS_MA_DOMAIN_PATH,
    LOGISTICS_MA_PROBLEM_PATH,
    LOGISTICS_MA_TRAJECTORY_PATH,
    STARCRAFT_DOMAIN_PATH,
    STARCRAFT_TRAJECTORY_PATH,
    TEST_NUMERIC_DEPOT_TRAJECTORY_WITH_LABELS,
)
from tests.multi_agent_tests.consts import WOODWORKING_AGENT_NAMES


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


@fixture()
def ma_combined_domain() -> Domain:
    return DomainParser(WOODWORKING_COMBINED_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def ma_combined_problem(ma_combined_domain: Domain) -> Problem:
    return ProblemParser(problem_path=WOODWORKING_COMBINED_PROBLEM_PATH, domain=ma_combined_domain).parse_problem()


@fixture()
def ma_trajectory_parser(ma_combined_domain: Domain, ma_combined_problem: Problem) -> TrajectoryParser:
    return TrajectoryParser(ma_combined_domain, ma_combined_problem)


@fixture()
def ma_depot_domain() -> Domain:
    return DomainParser(DEPOT_MA_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def ma_depot_problem(ma_depot_domain: Domain) -> Problem:
    return ProblemParser(problem_path=DEPOT_MA_PROBLEM_PATH, domain=ma_depot_domain).parse_problem()


@fixture()
def ma_depot_trajectory_parser(ma_depot_domain: Domain, ma_depot_problem: Problem) -> TrajectoryParser:
    return TrajectoryParser(ma_depot_domain, ma_depot_problem)


@fixture()
def ma_logistics_domain() -> Domain:
    return DomainParser(LOGISTICS_MA_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def ma_logistics_problem(ma_logistics_domain: Domain) -> Problem:
    return ProblemParser(problem_path=LOGISTICS_MA_PROBLEM_PATH, domain=ma_logistics_domain).parse_problem()


@fixture()
def ma_logistics_trajectory_parser(ma_logistics_domain: Domain, ma_logistics_problem: Problem) -> TrajectoryParser:
    return TrajectoryParser(ma_logistics_domain, ma_logistics_problem)


@fixture()
def starcraft_domain() -> Domain:
    domain_parser = DomainParser(STARCRAFT_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def starcraft_trajectory_parser(starcraft_domain: Domain) -> TrajectoryParser:
    return TrajectoryParser(starcraft_domain)


def test_parse_trajectory(trajectory_parser: TrajectoryParser):
    observation = trajectory_parser.parse_trajectory(TEST_NUMERIC_DEPOT_TRAJECTORY)
    assert len(observation.components) == 19


def test_parse_farmland_trajectory(farmland_trajectory_parser: TrajectoryParser):
    observation = farmland_trajectory_parser.parse_trajectory(FARMLAND_NUMERIC_TRAJECTORY)
    assert len(observation.components) == 12


def test_parse_ma_combined_trajectory(ma_trajectory_parser: TrajectoryParser):
    observation: MultiAgentObservation = ma_trajectory_parser.parse_trajectory(
        WOODWORKING_COMBINED_TRAJECTORY_PATH, executing_agents=WOODWORKING_AGENT_NAMES
    )
    assert len(observation.components) == 4
    print(observation.components[0].grounded_joint_action)


def test_parse_ma_combined_trajectory_creates_states_with_only_positive_predicates(
    ma_trajectory_parser: TrajectoryParser,
):
    observation = ma_trajectory_parser.parse_trajectory(
        WOODWORKING_COMBINED_TRAJECTORY_PATH, executing_agents=WOODWORKING_AGENT_NAMES
    )
    for component in observation.components:
        for predicate_set in component.previous_state.state_predicates.values():
            for predicate in predicate_set:
                assert predicate.is_positive

        for predicate_set in component.next_state.state_predicates.values():
            for predicate in predicate_set:
                assert predicate.is_positive


def test_parse_ma_combined_trajectory_parse_joint_actions_correctly_and_does_not_remove_actions_from_joint_actions(
    ma_logistics_trajectory_parser: TrajectoryParser,
):
    observation: MultiAgentObservation = ma_logistics_trajectory_parser.parse_trajectory(
        LOGISTICS_MA_TRAJECTORY_PATH,
        executing_agents=["apn1", "apn2", "tru1", "tru2", "tru3", "tru4", "tru5"],
    )
    for component in observation.components:
        joint_actions = component.grounded_joint_action
        if joint_actions.action_count == 1:
            assert "dummy" not in str(joint_actions)


def test_parse_depot_combined_trajectory(ma_depot_trajectory_parser: TrajectoryParser):
    observation = ma_depot_trajectory_parser.parse_trajectory(
        DEPOT_MA_TRAJECTORY_PATH,
        executing_agents=[
            "depot0",
            "distributor0",
            "distributor1",
            "distributor2",
            "distributor3",
            "truck0",
            "truck1",
            "truck2",
            "truck3",
        ],
    )
    assert "(clear pallet6)" not in observation.components[0].next_state.serialize()


def test_parse_starcraft_ma_trajectory_without_problem_objects_returns_correct_objects(
    starcraft_trajectory_parser: TrajectoryParser,
):
    observation = starcraft_trajectory_parser.parse_trajectory(
        STARCRAFT_TRAJECTORY_PATH,
        executing_agents=["agent0", "agent1", "agent2", "agent3", "agent4"],
    )
    assert observation.grounded_objects is not None
    assert len(observation.grounded_objects) == 5
    assert len(observation.components) == 40


def test_parse_depot_trajectory_with_trajectory_parser_without_problem_returns_correct_trajectory_data(
    domain: Domain,
):
    depot_trajectory_parser = TrajectoryParser(domain)
    observation = depot_trajectory_parser.parse_trajectory(TEST_NUMERIC_DEPOT_TRAJECTORY)
    assert observation.grounded_objects is not None
    assert len(observation.grounded_objects) == 15
    assert len(observation.components) == 19
    print(observation.grounded_objects.keys())


def test_parse_depot_trajectory_with_trajectory_parser_without_problem_and_with_trajectory_labels_returns_labelled_observation_with_successful_and_unsuccessful_transitions(
    domain: Domain,
):
    depot_trajectory_parser = TrajectoryParser(domain)
    observation = depot_trajectory_parser.parse_trajectory(
        TEST_NUMERIC_DEPOT_TRAJECTORY_WITH_LABELS, contain_transitions_status=True
    )
    assert observation.components[0].is_successful == True
    assert observation.components[1].is_successful == False


def test_parse_depot_trajectory_with_trajectory_parser_without_problem_and_without_labels_when_expecting_labels_raises_error(
    domain: Domain,
):
    depot_trajectory_parser = TrajectoryParser(domain)
    with pytest.raises(SyntaxError):
        depot_trajectory_parser.parse_trajectory(TEST_NUMERIC_DEPOT_TRAJECTORY, contain_transitions_status=True)


def test_parse_trajectory_when_not_supplied_both_trajectory_path_and_trajectory_string_raises_error(
    trajectory_parser: TrajectoryParser,
):
    with pytest.raises(ValueError):
        trajectory_parser.parse_trajectory(trajectory_file_path=None, trajectory_string=None)


def test_parse_trajectory_when_supplied_both_trajectory_path_and_trajectory_string_raises_error(
    trajectory_parser: TrajectoryParser,
):
    with pytest.raises(ValueError):
        trajectory_parser.parse_trajectory(
            trajectory_file_path=TEST_NUMERIC_DEPOT_TRAJECTORY, trajectory_string="(some trajectory string)"
        )


def test_parse_trajectory_when_supplied_trajectory_string_parses_correctly(trajectory_parser: TrajectoryParser):
    trajectory_string = (
        "((:init (= (current_load truck0) 0.0) (= (load_limit truck0) 411.0) (= (current_load truck1) 0.0) (= (load_limit truck1) 390.0) (= (weight crate0) 32.0) (= (weight crate1) 4.0) (= (weight crate2) 89.0) (= (weight crate3) 62.0) (= (fuel-cost ) 0.0) (at pallet1 distributor0) (at hoist2 distributor1) (at hoist0 depot0) (at crate3 distributor0) (at crate2 distributor1) (at truck0 depot0) (at pallet2 distributor1) (at hoist1 distributor0) (at crate0 depot0) (at crate1 distributor1) (at pallet0 depot0) (at truck1 depot0) (clear crate0) (clear crate2) (clear crate3) (available hoist2) )"
        "(operator: (drive truck0 depot0 distributor0))"
        "(:transition_status (success))"
        "(:state (= (current_load truck0) 0.0) (= (load_limit truck0) 411.0) (= (current_load truck1) 0.0) (= (load_limit truck1) 390.0) (= (weight crate0) 32.0) (= (weight crate1) 4.0) (= (weight crate2) 89.0) (= (weight crate3) 62.0) (= (fuel-cost ) 10.0) (at pallet1 distributor0) (at truck0 distributor0) (at hoist2 distributor1) (at hoist0 depot0) (at crate2 distributor1) (at pallet2 distributor1) (at hoist1 distributor0) (at crate1 distributor1) (at pallet0 depot0) (at truck1 depot0) (clear crate0) (clear crate2) (clear crate3) (available hoist2) )"
        ")"
    )
    observation = trajectory_parser.parse_trajectory(
        trajectory_file_path=None, trajectory_string=trajectory_string, contain_transitions_status=True
    )
    assert observation is not None
    assert len(observation.components) == 1
