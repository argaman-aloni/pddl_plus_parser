"""Module to convert MA domains into single agent domains"""
import logging
import random
from pathlib import Path

from pddl_plus_parser.exporters import DomainExporter
from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain, Predicate, Action

DUMMY_PREDICATE = Predicate(name="dummy-additional-predicate", signature={}, is_positive=True)


class MultiAgentDomainsConverter:
    """Converts multiple MA domains to single agent domain containing all the agents' data."""

    logger: logging.Logger
    domains_directory_path: Path

    def __init__(self, working_directory_path: Path):
        self.logger = logging.getLogger(__name__)
        self.domains_directory_path = working_directory_path

    def _add_dummy_action(self, domain: Domain) -> None:
        """Add a dummy action to the domain to make it a harder domain to learn.

        :param domain: the domain to add the dummy action to.
        """
        self.logger.debug("Adding a dummy action to the domain.")
        dummy_action = Action()
        dummy_action.name = "dummy-action"
        dummy_action.signature = {}
        dummy_action.add_effects = {DUMMY_PREDICATE}
        domain.actions[dummy_action.name] = dummy_action

    def _insert_dummy_predicate_to_actions(self, domain: Domain) -> None:
        """Insert the dummy predicate to all the actions in the domain.

        :param domain: the domain to insert the dummy predicate to.
        """
        self.logger.debug("Inserting the dummy predicate to random the actions in the domain.")
        for action in domain.actions.values():
            add_dummy_predicate = bool(random.randint(0, 1))
            if add_dummy_predicate:
                self.logger.debug(f"Adding the dummy predicate to the action - {action.name}")
                action.add_effects.add(DUMMY_PREDICATE)

    def locate_domains(self) -> Domain:
        """Locate only the domains when there is no need to also parse the problems."""
        combined_domain = Domain()
        for domain_path in self.domains_directory_path.glob("domain-*.pddl"):
            self.logger.debug(f"Working on the domain - {domain_path.stem}")
            domain_file_name = domain_path.stem
            agent_domain = DomainParser(domain_path=domain_path, partial_parsing=False,
                                        enable_disjunctions=True).parse_domain()

            combined_domain.name = agent_domain.name
            combined_domain.requirements = agent_domain.requirements
            combined_domain.types.update(agent_domain.types)
            combined_domain.predicates.update(agent_domain.predicates)
            combined_domain.constants.update(agent_domain.constants)
            combined_domain.actions.update(agent_domain.actions)
            combined_domain.functions.update(agent_domain.functions)

            self.logger.debug(f"extracted the domain - {domain_file_name}")

        combined_domain.predicates[DUMMY_PREDICATE.name] = DUMMY_PREDICATE
        self._add_dummy_action(combined_domain)
        self._insert_dummy_predicate_to_actions(combined_domain)
        return combined_domain

    def export_combined_domain(self) -> None:
        """Export the multi-agent domains to a single PDDL domain file."""
        combined_domain = self.locate_domains()
        DomainExporter().export_domain(combined_domain, self.domains_directory_path / f"combined_domain.pddl")
