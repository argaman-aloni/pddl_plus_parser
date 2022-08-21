"""Exports a problem object to a PDDL file."""
from pathlib import Path
from typing import NoReturn, List, Dict, Set, Union

from pddl_plus_parser.models import PDDLObject, GroundedPredicate, Problem, PDDLFunction, NumericalExpressionTree


class ProblemExporter:
    """Class that is able to export a domain to a correct PDDL file."""

    @staticmethod
    def write_objects(problem_objects: Dict[str, PDDLObject]) -> str:
        """Writes the definitions of the types according to the PDDL file format.

        :param problem_objects: the objects that are available in the learned domain.
        :return: the formatted string representing the objects in the PDDL problem file.
        """
        objects = []
        for pddl_object in problem_objects.values():
            objects.append(str(pddl_object))

        return "(:objects\n{objects_content}\n)\n".format(objects_content="\n\t".join(objects))

    def write_initial_state(self, initial_state_predicates: Dict[str, Set[GroundedPredicate]],
                            initial_state_fluents: Dict[str, PDDLFunction]) -> str:
        """Writes the definitions of the types according to the PDDL file format.

        :param initial_state_predicates: the objects that are available in the learned domain.
        :return: the formatted string representing the state in the PDDL problem file.
        :param initial_state_fluents: the numeric fluents in the initial state.
        """
        predicates_str = []
        fluents_str = []
        for grounded_predicates_set in initial_state_predicates.values():
            predicates_str.append(self.extract_state_predicates(grounded_predicates_set))

        for fluent in initial_state_fluents.values():
            fluents_str.append(fluent.state_representation)

        joint_state_str = "\n\t".join([*predicates_str, *fluents_str])
        return f"(:init\n\t{joint_state_str}\n\n)\n"

    def write_goal_state(self, goal_state_predicates: List[GroundedPredicate],
                         goal_state_fluents: Set[NumericalExpressionTree]) -> str:
        """Writes the definitions of the types according to the PDDL file format.

        :param goal_state_predicates: the objects that are available in the learned domain.
        :return: the formatted string representing the state in the PDDL problem file.
        :param goal_state_fluents: the numeric expressions in the goal state.
        """
        predicates_str = self.extract_state_predicates(goal_state_predicates)
        goal_fluents = [fluent.to_pddl() for fluent in goal_state_fluents]

        joint_goal = "\n\t\t".join([predicates_str, *goal_fluents])
        return f"(:goal\n\t(and\n\t{joint_goal}\t\t\n)\n)\n"

    @staticmethod
    def extract_state_predicates(state: Union[List[GroundedPredicate], Set[GroundedPredicate]]) -> str:
        """Extract the needed problem predicates for the PDDL file representation.

        :param state: the state to write in a PDDL format.
        :return: the strings of containing the state's data.
        """
        return "\n\t".join([predicate.untyped_representation for predicate in state])

    def extract_problem(self, problem: Problem) -> str:
        """Extract the problem str from the problem object.

        :param problem: the problem object to extract the data to a PDDL string representation.
        """
        problem_objects = self.write_objects(problem.objects)
        initial_state = self.write_initial_state(problem.initial_state_predicates, problem.initial_state_fluents)
        goal_state = self.write_goal_state(problem.goal_state_predicates, problem.goal_state_fluents)
        problem_data = f"(define (problem {problem.name}) (:domain {problem.domain.name})\n" \
                       f"{problem_objects}\n" \
                       f"{initial_state}\n" \
                       f"{goal_state}\n)"

        return problem_data

    def export_problem(self, problem: Problem, export_path: Path) -> NoReturn:
        """Export the domain object to a correct PDDL file.

        :param problem: the problem object to export to a PDDL file.
        :param export_path: the path to the file that the domain would be exported to.
        """
        problem_data = self.extract_problem(problem)

        with open(export_path, "wt") as export_problem_file:
            export_problem_file.write(problem_data)
