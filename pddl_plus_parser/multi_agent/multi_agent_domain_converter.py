"""Module to convert MA domains into single agent domains"""
import logging
from pathlib import Path
from typing import NoReturn

from pddl_plus_parser.exporters import DomainExporter
from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain


class MultiAgentDomainsConverter:
    """"""

    logger: logging.Logger
    domains_directory_path: Path

    def __init__(self, working_directory_path: Path):
        self.logger = logging.getLogger(__name__)
        self.domains_directory_path = working_directory_path

    def locate_domains(self) -> Domain:
        """Locate only the domains when there is no need to also parse the problems."""
        combined_domain = Domain()
        for domain_path in self.domains_directory_path.glob("domain-*.pddl"):
            self.logger.debug(f"Working on the domain - {domain_path.stem}")
            domain_file_name = domain_path.stem
            agent_domain = DomainParser(domain_path=domain_path, partial_parsing=False,
                                        enable_conjunctions=True).parse_domain()

            combined_domain.name = agent_domain.name
            combined_domain.requirements = agent_domain.requirements
            combined_domain.types.update(agent_domain.types)
            combined_domain.predicates.update(agent_domain.predicates)
            combined_domain.constants.update(agent_domain.constants)
            combined_domain.actions.update(agent_domain.actions)
            combined_domain.functions.update(agent_domain.functions)

            self.logger.debug(f"extracted the domain - {domain_file_name}")

        return combined_domain

    def export_combined_domain(self) -> NoReturn:
        """Export the domain into a file so that the model will be able to use it later."""
        combined_domain = self.locate_domains()
        DomainExporter().export_domain(combined_domain, self.domains_directory_path / f"combined_domain.pddl")
