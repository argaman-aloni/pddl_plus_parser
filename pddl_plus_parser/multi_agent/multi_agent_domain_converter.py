"""Module to convert MA domains into single agent domains"""
import logging
from pathlib import Path
from typing import Optional

from pddl_plus_parser.exporters import DomainExporter
from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain, Predicate, Action, Precondition

DUMMY_PREDICATE_NAME = "dummy-additional-predicate"
DUMMY_ADD_PREDICATE = Predicate(name=DUMMY_PREDICATE_NAME, signature={}, is_positive=True)
DUMMY_DEL_PREDICATE = Predicate(name=DUMMY_PREDICATE_NAME, signature={}, is_positive=False)


class MultiAgentDomainsConverter:
    """Converts multiple MA domains to single agent domain containing all the agents' data."""

    logger: logging.Logger
    domains_directory_path: Path

    def __init__(self, working_directory_path: Path):
        self.logger = logging.getLogger(__name__)
        self.domains_directory_path = working_directory_path

    def _add_dummy_actions(self, domain: Domain) -> None:
        """Add a dummy action to the domain to make it a harder domain to learn.

        :param domain: the domain to add the dummy action to.
        """
        self.logger.debug("Adding the dummy actions to the domain.")
        add_action = Action()
        add_action.name = "dummy-add-predicate-action"
        add_action.signature = {"?agent": domain.types["object"]}
        add_action.discrete_effects = {DUMMY_ADD_PREDICATE}
        domain.actions[add_action.name] = add_action

        delete_action = Action()
        delete_action.name = "dummy-del-predicate-action"
        delete_action.signature = {"?agent": domain.types["object"]}
        delete_action.discrete_effects = {DUMMY_DEL_PREDICATE}
        domain.actions[delete_action.name] = delete_action

    def locate_domains(self, add_dummy_actions: bool = False) -> Domain:
        """Locate only the domains when there is no need to also parse the problems.

        :param add_dummy_actions: whether to add dummy actions to the domain.
        """
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

        if add_dummy_actions:
            combined_domain.predicates[DUMMY_ADD_PREDICATE.name] = DUMMY_ADD_PREDICATE
            self._add_dummy_actions(combined_domain)

        return combined_domain

    def export_combined_domain(self, add_dummy_actions: bool = False, output_folder: Optional[Path] = None) -> Path:
        """Export the multi-agent domains to a single PDDL domain file.

        :param add_dummy_actions: whether to add dummy actions to the domain.
        :param output_folder: the folder to export the combined domain to.
        :return: the path to the exported domain file.
        """
        combined_domain = self.locate_domains(add_dummy_actions)
        output_folder_path = output_folder if output_folder is not None else self.domains_directory_path
        domain_path = output_folder_path / f"{combined_domain.name.lower()}_combined_domain.pddl"
        DomainExporter().export_domain(combined_domain, domain_path)
        return domain_path
