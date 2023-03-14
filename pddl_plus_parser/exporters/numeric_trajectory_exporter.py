"""Module that encapsulates the numeric trajectory functionalities."""
import logging
from pathlib import Path
from typing import List, NoReturn, Optional, Dict

from pddl_plus_parser.models import Domain, Problem, Operator, State, ActionCall, PDDLObject


def parse_action_call(action_call: str) -> ActionCall:
    """Parses the string representing the action call in the plan sequence.

    :param action_call: the string representing the action call.
    :return: the object representing the action name and its parameters.
    """
    action_data = action_call.lower().replace("(", " ( ").replace(")", " ) ").split()
    action_data = action_data[1:-1]
    return ActionCall(name=action_data[0], grounded_parameters=action_data[1:])


class TrajectoryTriplet:
    """Class representing a single trajectory triplet."""
    previous_state: State
    operator: Operator
    next_state: State

    def __init__(self, previous_state: State, op: Operator, next_state: State):
        self.previous_state = previous_state
        self.operator = op
        self.next_state = next_state

    def __str__(self):
        return f"previous state: {self.previous_state.serialize()}\n" \
               f"operator: {str(self.operator)}\n" \
               f"next state: {self.next_state.serialize()}"


class TrajectoryExporter:
    """Export trajectories in the appropriate format."""

    domain: Domain
    allow_invalid_actions: bool
    logger: logging.Logger

    def __init__(self, domain: Domain, allow_invalid_actions: bool = False):
        self.domain = domain
        self.allow_invalid_actions = allow_invalid_actions
        self.logger = logging.getLogger(__name__)

    def _read_plan(self, plan_file_path: Path) -> List[str]:
        """Read the plan file and exports the lines with the actions.

        :param plan_path: the path to the plan file.
        :return: the action sequence.
        """
        self.logger.debug(f"Reading the plan in the path {plan_file_path}")
        with open(plan_file_path, "rt") as plan_file:
            return plan_file.readlines()

    def create_single_triplet(self, previous_state: State, action_call: str,
                              problem_objects: Dict[str, PDDLObject]) -> TrajectoryTriplet:
        """Create a single trajectory triplet by applying the action on the input state.

        :param previous_state: the state that the action is being applied on.
        :param action_call: the string representation of the grounded action call.
        :param problem_objects: the objects of the problem.
        :return: the new triplet containing (s,a,s').
        """
        self.logger.info(f"Trying to apply the action - {action_call} on the state - {previous_state.serialize()}")
        action_descriptor = parse_action_call(action_call)
        operator = Operator(action=self.domain.actions[action_descriptor.name],
                            domain=self.domain,
                            grounded_action_call=action_descriptor.parameters,
                            problem_objects=problem_objects)
        try:
            next_state = operator.apply(previous_state, allow_inapplicable_actions=self.allow_invalid_actions)

        except ValueError:
            self.logger.debug("In case an action is inapplicable, the state remains unchanged.")
            next_state = State(predicates=previous_state.state_predicates,
                               fluents=previous_state.state_fluents, is_init=False)

        return TrajectoryTriplet(previous_state=previous_state,
                                 op=operator,
                                 next_state=next_state)

    def parse_plan(self, problem: Problem, plan_path: Optional[Path] = None,
                   action_sequence: Optional[List[str]] = None) -> List[TrajectoryTriplet]:
        """Parse the input plan file to create the trajectory.

        :return: the list of triplets that was generated using the plan.
        """
        self.logger.info("Parsing the plan to extract the grounded operators.")
        plan_actions = action_sequence if action_sequence is not None else self._read_plan(plan_path)
        initial_state_predicates = problem.initial_state_predicates
        initial_state_numeric_fluents = problem.initial_state_fluents
        previous_state = State(predicates=initial_state_predicates, fluents=initial_state_numeric_fluents, is_init=True)
        triplets = []
        self.logger.debug("Starting to create the trajectory triplets.")
        for grounded_action_call in plan_actions:
            triplet = self.create_single_triplet(previous_state, grounded_action_call, problem.objects)
            triplets.append(triplet)
            previous_state = triplet.next_state

        return triplets

    @staticmethod
    def export(triplets: List[TrajectoryTriplet]) -> List[str]:
        """Export the input triplets as a valid trajectory object.

        :param triplets: the objects representing the triplets generated from the plan sequence.
        :return: a list of strings representing the trajectory.
        """
        serialized_trajectory = []
        first_state = triplets[0].previous_state
        serialized_trajectory.append(first_state.serialize())
        for triplet in triplets:
            serialized_trajectory.append(f"(operator: {str(triplet.operator)})\n")
            serialized_trajectory.append(triplet.next_state.serialize())

        serialized_trajectory[0] = f"({serialized_trajectory[0]}"
        serialized_trajectory[-1] = f"{serialized_trajectory[-1]})"
        return serialized_trajectory

    def export_to_file(self, triplets: List[TrajectoryTriplet], output_path: Path) -> NoReturn:
        """Export the trajectory to a file.

        :param triplets: the trajectory triples.
        :param output_path: the path to the output file.
        """
        trajectory_lines = self.export(triplets)
        with open(output_path, "wt") as output_path:
            output_path.writelines(trajectory_lines)
