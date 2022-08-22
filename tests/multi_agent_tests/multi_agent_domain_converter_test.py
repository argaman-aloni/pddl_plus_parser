"""Module test for the multi-agent to single agent domain convertion."""
from pytest import fixture

from pddl_plus_parser.multi_agent import MultiAgentDomainsConverter
from tests.multi_agent_tests.consts import MULTI_AGENT_DATA_DIRECTORY


@fixture()
def domain_converter() -> MultiAgentDomainsConverter:
    return MultiAgentDomainsConverter(MULTI_AGENT_DATA_DIRECTORY)


def test_locate_domains_returns_domain_with_correct_name(domain_converter: MultiAgentDomainsConverter):
    """Test that the locate_domains method returns a domain with a correct name."""
    domain = domain_converter.locate_domains()
    assert domain.name == "woodworking"


def test_locate_domains_returns_all_private_and_public_predicates(domain_converter: MultiAgentDomainsConverter):
    """Test that the locate_domains method returns a domain with all private and public predicates."""
    domain = domain_converter.locate_domains()
    assert "grind-treatment-change" in domain.predicates
    assert "boardsize-successor" in domain.predicates
    assert len(domain.predicates) == 14


def test_locate_domains_returns_agents_actions(domain_converter: MultiAgentDomainsConverter):
    """Test that the locate_domains method returns a domain with all agents' actions."""
    domain = domain_converter.locate_domains()
    assert "do-grind" in domain.actions
    assert "do-saw-small" in domain.actions
    assert "do-saw-medium" in domain.actions
    assert "do-saw-large" in domain.actions
