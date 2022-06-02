"""Parse the output of the mtericFF planner so that the algorithms will be able to use it."""
import logging
import re
import sys

from pathlib import Path
from typing import NoReturn, List, Tuple

PLAN_COMPONENT_REGEX = r"\d: ([\w+\s?-]+)\n"
VALID_PLAN_FOUND_PATTERN = "ff: found legal plan as follows"
NO_SOLUTION_OPTIONS = ["problem proven unsolvable.",
                       "ff: goal can be simplified to FALSE. No plan will solve it",
                       "all increasers applied yet goal not fulfilled"]
NO_SOLUTION_FOUND_PATTERN = "problem proven unsolvable."
NO_SOLUTION_FOUND_PATTERN_2 = "ff: goal can be simplified to FALSE. No plan will solve it"
NO_SOLUTION_FOUND_PATTERN_3 = "all increasers applied yet goal not fulfilled"


class MetricFFParser:
    """Parse metricFF plans and exports then into standard output file."""

    logger: logging.Logger

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _open_plan_file(input_path: Path) -> str:
        """Safely open the file and returns its content.

        :param input_path: the path to the log file.
        :return: the file content.
        """
        with open(input_path, "rt") as interm_plan_file:
            return interm_plan_file.read()

    def _parse_plan_content(self, planner_output) -> List[str]:
        """Parse the content of the file and export the action sequence.

        :param planner_output: the file content with the possible action sequence.
        :return: the action sequence.
        """
        matches = re.finditer(PLAN_COMPONENT_REGEX, planner_output, re.MULTILINE)
        plan_seq = []
        for match in matches:
            action_sequence = match.group(1)
            self.logger.debug(f"action sequence - {action_sequence}")
            plan_seq.append(f"({action_sequence.lower().strip()})\n")

        if len(plan_seq) == 0:
            return []

        return plan_seq

    def parse_plan(self, input_path: Path, output_path: Path) -> NoReturn:
        """Parse the output file and exports a plan if exists.

        :param input_path: the path to the output log of metricFF planner.
        :param output_path: the path to the output plan file.
        """
        planner_output = self._open_plan_file(input_path)
        action_sequence = self._parse_plan_content(planner_output)
        if len(action_sequence) == 0:
            return

        with open(output_path, "wt") as output_file:
            output_file.writelines(action_sequence)

    def get_solving_status(self, input_path: Path) -> Tuple[str, List[str]]:
        """Validates if the plan file contains a valid plan.

        :param input_path: the path to the input file.
        :return: "ok" if a plan exists, "timeout" if the solver timed out or "no-solution"
            if there is no solution for the problem as well as the action sequence.
        """
        file_content = self._open_plan_file(input_path)
        plan_found = re.search(VALID_PLAN_FOUND_PATTERN, file_content, re.MULTILINE)
        if plan_found is not None:
            action_sequence = self._parse_plan_content(file_content)
            return "ok", action_sequence

        for option in NO_SOLUTION_OPTIONS:
            no_solution_match = re.search(option, file_content, re.MULTILINE)
            if no_solution_match is not None:
                return "no-solution", []

        return "timeout", []


if __name__ == '__main__':
    MetricFFParser().parse_plan(Path(sys.argv[1]), Path(sys.argv[2]))
