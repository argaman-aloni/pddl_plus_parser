"""Module that encapsulates the multi-agent trajectory functionalities."""
import logging
import re
from pathlib import Path
from typing import List, Optional, Union, Dict

from pddl_plus_parser.models import Domain, Problem, Operator, State, JointActionCall, ActionCall, NOP_ACTION, \
    NOPOperator, PDDLObject
from pddl_plus_parser.multi_agent.common import create_initial_state, apply_actions

JOINT_ACTION_REGEX = r"\(([\w+\s?-]+)\)"


def parse_action_call(joint_action_call: str) -> JointActionCall:
    """Parses the string representing the joint action call in the plan sequence.

    :param joint_action_call: the string representing the joint action.
    :return: the object representing the action name and its parameters.
    """
    matches = re.finditer(JOINT_ACTION_REGEX, joint_action_call)
    single_agent_actions = []
    for match in matches:
        single_agent_action_data = match.group(1)
        action_components = single_agent_action_data.split()
        action_name = action_components[0]
        single_agent_actions.append(ActionCall(name=action_name, grounded_parameters=action_components[1:]))

    return JointActionCall(single_agent_actions)


class MultiAgentTrajectoryTriplet:
    """Class representing a single multi-agent trajectory triplet."""
    previous_state: State
    joint_action: List[Union[Operator, NOPOperator]]
    next_state: State

    def __init__(self, previous_state: State, ops: List[Operator], next_state: State):
        self.previous_state = previous_state
        self.joint_action = ops
        self.next_state = next_state

    def __str__(self):
        return f"previous state: {self.previous_state.serialize()}\n" \
               f"operators: {[str(op) for op in self.joint_action]}\n" \
               f"next state: {self.next_state.serialize()}"


class MultiAgentTrajectoryExporter:
    """Export multi-agent trajectories in the appropriate format."""

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

    def create_multi_agent_triplet(self, previous_state: State, action_call: str,
                                   problem_objects: Dict[str, PDDLObject]) -> MultiAgentTrajectoryTriplet:
        """Create a single trajectory triplet by applying the joint action on the input state and combining the effects.

        :param previous_state: the state that the action is being applied on.
        :param action_call: the string representation of the grounded joint action call.
        :param problem_objects: the objects in the problem.
        :return: the new triplet containing (s,<a1, a2,..., am>,s').
        """
        self.logger.info(f"Trying to apply the action - {action_call} on the state - {previous_state.serialize()}")
        joint_action = parse_action_call(action_call)
        executed_actions = [ActionCall(name=op.name, grounded_parameters=op.parameters) for op in
                            joint_action.actions if op.name != NOP_ACTION]
        operators = []
        for sa_action in joint_action.actions:
            if sa_action.name == NOP_ACTION:
                operators.append(NOPOperator())
                continue

            operators.append(Operator(action=self.domain.actions[sa_action.name], domain=self.domain,
                                      grounded_action_call=sa_action.parameters, problem_objects=problem_objects))
        next_state = apply_actions(self.domain, previous_state, executed_actions)
        return MultiAgentTrajectoryTriplet(previous_state=previous_state, ops=operators, next_state=next_state)

    def parse_plan(self, problem: Problem, plan_path: Optional[Path] = None,
                   action_sequence: Optional[List[str]] = None) -> List[MultiAgentTrajectoryTriplet]:
        """Parse the input plan file to create the trajectory.

        :return: the list of triplets that was generated using the plan.
        """
        self.logger.info("Parsing the plan to extract the grounded operators.")
        plan_actions = action_sequence if action_sequence is not None else self._read_plan(plan_path)
        previous_state = create_initial_state(problem)
        triplets = []
        self.logger.debug("Starting to create the trajectory triplets.")
        for grounded_action_call in plan_actions:
            triplet = self.create_multi_agent_triplet(previous_state, grounded_action_call,
                                                      problem_objects=problem.objects)
            triplets.append(triplet)
            previous_state = triplet.next_state

        return triplets

    @staticmethod
    def export(triplets: List[MultiAgentTrajectoryTriplet]) -> List[str]:
        """Export the input triplets as a valid trajectory object.

        :param triplets: the objects representing the triplets generated from the plan sequence.
        :return: a list of strings representing the trajectory.
        """
        serialized_trajectory = []
        first_state = triplets[0].previous_state
        serialized_trajectory.append(first_state.serialize())
        for triplet in triplets:
            operators = " ".join([str(op) for op in triplet.joint_action])
            serialized_trajectory.append(f"(operators: {operators})\n")
            serialized_trajectory.append(triplet.next_state.serialize())

        serialized_trajectory[0] = f"({serialized_trajectory[0]}"
        serialized_trajectory[-1] = f"{serialized_trajectory[-1]})"
        return serialized_trajectory

    def export_to_file(self, triplets: List[MultiAgentTrajectoryTriplet], output_path: Path) -> None:
        """Export the trajectory to a file.

        :param triplets: the trajectory triples.
        :param output_path: the path to the output file.
        """
        trajectory_lines = self.export(triplets)
        with open(output_path, "wt") as output_path:
            output_path.writelines(trajectory_lines)
