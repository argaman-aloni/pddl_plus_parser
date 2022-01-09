"""Module that contains the parser for PDDL+ domain files."""
from pathlib import Path

from lisp_parsers import PDDLTokenizer
from models import Domain


class DomainParser:
    """Class that parses PDDL+ domain files."""

    tokenizer: PDDLTokenizer

    def __init__(self, domain_path: Path):
        self.tokenizer = PDDLTokenizer(domain_path)

    def parse_domain(self) -> Domain:
        """The main entry point that parses the domain file and returns the resulting Domain object.

        :return: the domain object extracted from the tokens.
        """
        domain_expressions = self.tokenizer.parse()
