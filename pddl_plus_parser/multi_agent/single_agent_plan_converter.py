"""Module to convert single agent plans to multi-agent plans with joint actions."""
import logging
import re
from pathlib import Path
from typing import List, Tuple, Set

from pddl_plus_parser.models import Domain, ActionCall, Operator, JointActionCall, NOP_ACTION, Problem, State
from pddl_plus_parser.multi_agent.common import create_initial_state, apply_actions

PLAN_COMPONENT_REGEX = r"[\d+ : ]?\(([\w+\s?-]+)\)"


class PlanConverter:
    """Class that converts single agent plans to multi-agent plans with joint actions."""

    ma_domain: Domain
    logger: logging.Logger

    def __init__(self, ma_domain: Domain):
        self.ma_domain = ma_domain
        self.logger = logging.getLogger(__name__)

    def _extract_plan_actions(self, plan: str, agent_names: List[str]) -> List[Tuple[ActionCall, str]]:
        """Extracts the actions from the multi-agent plan.

        :param plan: the multi-agent plan.
        :param agent_names: the names of the agents.
        :return: the list tuples containing the action and the agent that executes it.
        """
        self.logger.info(f"Extracting the actions from the multi-agent plan:\n{plan}")
        matches = re.finditer(PLAN_COMPONENT_REGEX, plan, re.MULTILINE)
        plan_seq = []
        for match in matches:
            action_sequence = match.group(1)
            self.logger.debug(f"action sequence - {action_sequence}")
            action_components = action_sequence.lower().split()
            action_name = action_components[0]
            action_parameters = action_components[1:]
            # assuming that only one agent executes an action
            executing_agent = [param for param in action_parameters if param in agent_names][0]
            plan_seq.append((ActionCall(action_name, action_parameters), executing_agent))

        return plan_seq

    @staticmethod
    def _validate_two_sided_relation(
            positive_preconditions: Set[str], negative_preconditions: Set[str], add_effects: Set[str],
            delete_effects: Set[str], next_action_pos_preconditions: Set[str],
            next_action_neg_preconditions: Set[str], next_action_add_effects: List[str],
            next_action_del_effects: List[str]) -> bool:
        """

        :param positive_preconditions:
        :param negative_preconditions:
        :param add_effects:
        :param delete_effects:
        :param next_action_pos_preconditions:
        :param next_action_neg_preconditions:
        :param next_action_add_effects:
        :param next_action_del_effects:
        :return:
        """
        if len(negative_preconditions.intersection(next_action_pos_preconditions)) > 0 or \
                len(positive_preconditions.intersection(next_action_neg_preconditions)) > 0 or \
                len(add_effects.intersection(next_action_del_effects)) > 0 or \
                len(delete_effects.intersection(next_action_add_effects)) > 0 or \
                len(positive_preconditions.intersection(next_action_del_effects)) > 0 or \
                len(negative_preconditions.intersection(next_action_add_effects)) > 0 or \
                len(next_action_pos_preconditions.intersection(delete_effects)) > 0 or \
                len(next_action_neg_preconditions.intersection(add_effects)) > 0:
            return False

        return True

    def _validate_well_defined_action_literals(self, combined_actions: List[ActionCall], next_action: Operator) -> bool:
        """Validates whether the actions' grounded literals are well-defined.

        We define a contradiction as the following:
            If a fluent and its negation exist in the same time, than it is considered a contradiction.

        Note: extending to numeric actions is easy when considering that two actions cannot change the same function at
        the same time.

        :param combined_actions: the currently constructed joint action.
        :param next_action: the new action to consider to add to the joint action.
        :return: whether the grounded literals are well-defined.
        """
        self.logger.debug("Validating that the literals are well-defined!")
        positive_preconditions = set()
        negative_preconditions = set()
        add_effects = set()
        delete_effects = set()

        for action_call in combined_actions:
            if action_call.name == NOP_ACTION:
                continue

            op = Operator(self.ma_domain.actions[action_call.name], self.ma_domain, action_call.parameters)
            op.ground()
            positive_preconditions.update([p.untyped_representation for p in op.grounded_positive_preconditions])
            negative_preconditions.update([p.untyped_representation for p in op.grounded_negative_preconditions])
            add_effects.update([p.untyped_representation for p in op.grounded_add_effects])
            delete_effects.update([p.untyped_representation for p in op.grounded_delete_effects])

        next_action_pos_preconditions = set(
            [p.untyped_representation for p in next_action.grounded_positive_preconditions])
        next_action_neg_preconditions = set(
            [p.untyped_representation for p in next_action.grounded_negative_preconditions])
        next_action_add_effects = [p.untyped_representation for p in next_action.grounded_add_effects]
        next_action_del_effects = [p.untyped_representation for p in next_action.grounded_delete_effects]

        return self._validate_two_sided_relation(
            positive_preconditions, negative_preconditions, add_effects, delete_effects, next_action_pos_preconditions,
            next_action_neg_preconditions, next_action_add_effects, next_action_del_effects)

    def _validate_well_defined_joint_action(self, current_state: State,
                                            combined_actions: List[ActionCall], next_action: ActionCall,
                                            next_executing_agent: str, agent_names: List[str],
                                            should_validate_concurrency_constraint: bool = True) -> bool:
        """Validates if the joint action is well-defined.

        Note: the method in which the algorithm validates if a joint-action is well-defined is as follows:
            1. if the next action's executing agent already appears in the joint action,
                then the joint action is not well-defined.
            2. for each grounded literal in the joint action, if the preconditions contain contradictions,
                or the effects contain contradictions, then the joint action is not well-defined.

        We define a contradiction as the following:
            If a fluent and its negation exist in the same time, then it is considered a contradiction.
            Another example for a contradiction is a violation of the concurrency constraint which means, in our case,
            that more than one agent is interacting with an object.

        :param combined_actions: the joint action that is currently constructed.
        :param next_action: the new action to consider to add to the joint action.
        :param next_executing_agent: the agent that executes the new action.
        :param agent_names: the names of the agents.
        :param should_validate_concurrency_constraint: whether to validate the concurrency constraint.
        :return: whether the joint action with the new action is well-defined.
        """
        self.logger.info(f"Validating the joint action with the new action {str(next_action)}")
        next_agent_action_index = agent_names.index(next_executing_agent)
        if combined_actions[next_agent_action_index].name != NOP_ACTION:
            self.logger.debug("The agent already executes an action in the joint action")
            return False

        joint_action = JointActionCall(actions=combined_actions)
        if len(set(joint_action.joint_parameters).intersection(set(next_action.parameters))) > 0 \
                and should_validate_concurrency_constraint:
            self.logger.debug("The new action violates the concurrency constraint!")
            return False

        next_action_op = Operator(self.ma_domain.actions[next_action.name], self.ma_domain, next_action.parameters)
        next_action_op.ground()
        if not next_action_op.is_applicable(current_state):
            return False

        return self._validate_well_defined_action_literals(combined_actions, next_action_op)

    def _create_joint_actions(self, problem: Problem, plan_actions: List[Tuple[ActionCall, str]],
                              agent_names: List[str],
                              should_validate_concurrency_constraint: bool = True) -> List[JointActionCall]:
        """Creates the joint actions from the single agent actions.

        :param plan_actions: the single agent actions.
        :param agent_names: the names of the agents.
        :param should_validate_concurrency_constraint: whether to validate the concurrency constraint.
        :return: the joint actions.
        """
        self.logger.info("Creating the joint actions from the single agent action plan!")
        joint_actions = []
        current_state = create_initial_state(problem)
        while len(plan_actions) > 0:
            self.logger.debug("Initializing joint action to have only NOP for all the agents")
            joint_action = [ActionCall(NOP_ACTION, []) for _ in agent_names]
            action, agent = plan_actions.pop(0)
            joint_action[agent_names.index(agent)] = action

            if len(plan_actions) == 0:
                joint_actions.append(JointActionCall(joint_action))
                break

            next_action, next_executing_agent = plan_actions[0]
            while self._validate_well_defined_joint_action(current_state, joint_action, next_action,
                                                           next_executing_agent,
                                                           agent_names, should_validate_concurrency_constraint):
                joint_action[agent_names.index(next_executing_agent)] = plan_actions.pop(0)[0]

            current_state = apply_actions(self.ma_domain, current_state, [action for action in joint_action
                                                                          if action.name != NOP_ACTION])
            joint_actions.append(JointActionCall(joint_action))

        return joint_actions

    def convert_plan(self, problem: Problem, plan_file_path: Path, agent_names: List[str],
                     should_validate_concurrency_constraint: bool = True) -> List[JointActionCall]:
        """Converts a single agent plan to a multi-agent plan containing joint actions.

        :param problem: the problem that the plan solves.
        :param plan_file_path: the path to the original single agent plan.
        :param agent_names: the names of the agents that appear in the plan.
        :param should_validate_concurrency_constraint: whether to validate the concurrency constraint.
        :return: the list of joint actions describing the multi-agent plan.
        """
        with open(plan_file_path, "rt") as plan_file:
            plan_data = self._extract_plan_actions(plan_file.read(), agent_names)
            plan_actions = self._create_joint_actions(problem, plan_data, agent_names,
                                                      should_validate_concurrency_constraint)

        return plan_actions

    @staticmethod
    def export_plan(plan_file_path: Path, plan_actions: List[JointActionCall]):
        """Exports the multi-agent plan to a file.

        :param plan_file_path: the path to the file to export the plan to.
        :param plan_actions: the list of joint actions to export.
        """
        with open(plan_file_path, "wt") as plan_file:
            plan_file.writelines([f"{str(joint_action)}\n" for joint_action in plan_actions])
