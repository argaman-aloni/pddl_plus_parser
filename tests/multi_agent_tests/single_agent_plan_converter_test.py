"""Module test for the single agent plan converter."""

from pytest import fixture

from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain
from pddl_plus_parser.multi_agent import PlanConverter
from tests.multi_agent_tests.consts import SOKOBAN_DOMAIN_FILE_PATH, SOKOBAN_UNPARSED_PLAN_PATH, \
    WOODWORKING_DOMAIN_FILE_PATH, WOODWORKING_UNPARSED_PLAN_PATH

SOKOBAN_AGENT_NAMES = ["player-01", "player-02"]
WOODWORKING_AGENT_NAMES = ["glazer0", "grinder0", "highspeed-saw0", "immersion-varnisher0", "planer0", "saw0",
                           "spray-varnisher0"]


@fixture()
def sokoban_domain() -> Domain:
    domain_parser = DomainParser(SOKOBAN_DOMAIN_FILE_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def sokoban_plan_converter(sokoban_domain: Domain) -> PlanConverter:
    return PlanConverter(sokoban_domain)


@fixture()
def woodworking_domain() -> Domain:
    domain_parser = DomainParser(WOODWORKING_DOMAIN_FILE_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def woodworking_plan_converter(woodworking_domain: Domain) -> PlanConverter:
    return PlanConverter(woodworking_domain)


def test_convert_plan_does_not_remove_actions_from_original_plan(sokoban_plan_converter: PlanConverter):
    joint_actions = sokoban_plan_converter.convert_plan(SOKOBAN_UNPARSED_PLAN_PATH, agent_names=SOKOBAN_AGENT_NAMES)
    assert sum([action.action_count for action in joint_actions]) == 28


def test_convert_plan_reduce_plan_length(sokoban_plan_converter: PlanConverter):
    joint_actions = sokoban_plan_converter.convert_plan(SOKOBAN_UNPARSED_PLAN_PATH, agent_names=SOKOBAN_AGENT_NAMES)
    assert len(joint_actions) < 28


def test_convert_plan_does_not_have_joint_actions_with_same_agent(sokoban_plan_converter: PlanConverter):
    joint_actions = sokoban_plan_converter.convert_plan(SOKOBAN_UNPARSED_PLAN_PATH, agent_names=SOKOBAN_AGENT_NAMES)
    for joint_action in joint_actions:
        assert len([param for param in joint_action.joint_parameters if param == SOKOBAN_AGENT_NAMES[0]]) <= 1
        assert len([param for param in joint_action.joint_parameters if param == SOKOBAN_AGENT_NAMES[1]]) <= 1


def test_convert_plan_does_not_remove_actions_from_original_plan_when_domain_contains_constants(
        woodworking_plan_converter: PlanConverter):
    joint_actions = woodworking_plan_converter.convert_plan(WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)
    assert sum([action.action_count for action in joint_actions]) == 6


def test_convert_plan_reduce_plan_length_when_domain_contains_constants(
        woodworking_plan_converter: PlanConverter):
    joint_actions = woodworking_plan_converter.convert_plan(WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)
    assert len(joint_actions) < 6


def test_convert_plan_does_not_have_joint_actions_with_same_agent_when_domain_contains_constants(
        woodworking_plan_converter: PlanConverter):
    joint_actions = woodworking_plan_converter.convert_plan(WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)
    for joint_action in joint_actions:
        for agent_name in WOODWORKING_AGENT_NAMES:
            assert len([param for param in joint_action.joint_parameters if param == agent_name]) <= 1


def test_convert_plan_produces_readable_plan(woodworking_plan_converter: PlanConverter):
    joint_actions = woodworking_plan_converter.convert_plan(WOODWORKING_UNPARSED_PLAN_PATH,
                                                            agent_names=WOODWORKING_AGENT_NAMES)

    print()
    for joint_action in joint_actions:
        print(joint_action)
