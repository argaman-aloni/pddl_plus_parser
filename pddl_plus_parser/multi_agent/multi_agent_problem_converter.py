"""Module to convert MA domains into single agent domains"""
import logging
from pathlib import Path
from typing import NoReturn

from pddl_plus_parser.exporters import ProblemExporter
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import Problem


class MultiAgentProblemsConverter:
    """Manages the multiple agents and their domain and problems."""

    logger: logging.Logger
    problems_directory_path: Path

    def __init__(self, working_directory_path: Path, problem_file_prefix: str):
        self.logger = logging.getLogger(__name__)
        self.problems_directory_path = working_directory_path
        self.problem_file_prefix = problem_file_prefix

    def combine_problems(self, combined_domain_path: Path) -> Problem:
        """Converts the MA problems to one single agent problem with combined initial state and goals.

        :return: the problem that represents the combination of all of the agents' problems.
        """
        combined_domain = DomainParser(domain_path=combined_domain_path, partial_parsing=False).parse_domain()
        combined_problem = Problem(domain=combined_domain)
        for problem_file_path in self.problems_directory_path.glob(f"{self.problem_file_prefix}-*.pddl"):
            agent_problem = ProblemParser(problem_path=problem_file_path, domain=combined_domain).parse_problem()
            combined_problem.name = agent_problem.name
            combined_problem.objects.update(agent_problem.objects)
            combined_problem.initial_state_fluents.update(agent_problem.initial_state_fluents)
            for predicate, grounded_predicates in agent_problem.initial_state_predicates.items():
                combined_problem.initial_state_predicates[predicate].update(grounded_predicates)

            combined_problem.goal_state_predicates.extend(agent_problem.goal_state_predicates)
            combined_problem.goal_state_predicates = list(set(combined_problem.goal_state_predicates))
            combined_problem.goal_state_fluents.update(agent_problem.goal_state_fluents)

        return combined_problem

    def export_combined_problem(self, combined_domain_path: Path) -> NoReturn:
        """

        :param combined_domain_path:
        :return:
        """
        combined_problem = self.combine_problems(combined_domain_path)
        ProblemExporter().export_problem(combined_problem, self.problems_directory_path / f"combined_problem.pddl")