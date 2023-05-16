"""module to represent an operator that can apply actions and change state objects."""
import logging
from typing import List, Set, Dict, Optional

from .conditional_effect import UniversalEffect
from .grounded_effect import GroundedEffect
from .grounded_precondition import GroundedPrecondition
from .pddl_action import Action
from .pddl_domain import Domain
from .pddl_object import PDDLObject
from .pddl_state import State


class Operator:
    action: Action
    domain: Domain
    grounded_call_objects: List[str]
    grounded: bool
    logger: logging.Logger

    # These fields are constructed after the grounding process.
    grounded_preconditions: GroundedPrecondition
    grounded_effects: Set[GroundedEffect]
    lifted_universal_effects: Set[UniversalEffect]
    problem_objects: Dict[str, PDDLObject]

    def __init__(self, action: Action, domain: Domain, grounded_action_call: List[str],
                 problem_objects: Optional[Dict[str, PDDLObject]] = None):
        self.action = action
        self.domain = domain
        self.grounded_call_objects = grounded_action_call
        self.grounded = False
        self.problem_objects = problem_objects
        self.grounded_effects = set()
        self.lifted_universal_effects = self.action.universal_effects
        self.logger = logging.getLogger(__name__)

    @property
    def name(self) -> str:
        return self.action.name

    @property
    def typed_action_call(self) -> str:
        signature_str_items = [f"{parameter_name} - {str(parameter_type)}"
                               for parameter_name, parameter_type in
                               zip(self.grounded_call_objects, self.action.signature.values())]
        return f"({self.name} {' '.join(signature_str_items)})"

    def __str__(self):
        called_objects = " ".join(self.grounded_call_objects)
        return f"({self.name} {called_objects})"

    def _ground_conditional_effects(self, parameters_map: Dict[str, str]) -> Set[GroundedEffect]:
        """Grounds a single conditional effect.

        :param parameters_map: the mapping between the action's parameters and the objects using which the action was
            called.
        :return: a grounded conditional effect.
        """
        effects = set()
        simple_grounded_effects = GroundedEffect(
            lifted_antecedents=None, lifted_discrete_effects=self.action.discrete_effects,
            lifted_numeric_effects=self.action.numeric_effects, domain=self.domain, action=self.action)
        simple_grounded_effects.ground_conditional_effect(parameters_map)
        effects.add(simple_grounded_effects)

        for conditional_effect in self.action.conditional_effects:
            grounded_effect = GroundedEffect(
                lifted_antecedents=conditional_effect.antecedents,
                lifted_discrete_effects=conditional_effect.discrete_effects,
                lifted_numeric_effects=conditional_effect.numeric_effects, domain=self.domain, action=self.action)
            grounded_effect.ground_conditional_effect(parameters_map)
            effects.add(grounded_effect)

        return effects

    def _apply_universal_effects(self, previous_state: State, current_state: State) -> None:
        """Updates the state predicates based on the universal effects of the action.

        :param previous_state: the state that the action is being applied on.
        :param current_state: the state that will change according to the action's effects.
        """
        if self.problem_objects is None:
            self.logger.warning("Did not receive the problem object so cannot apply the universal effects.")
            return

        for pddl_object in self.problem_objects.values():
            self.logger.debug(f"Trying to apply the action's universal effects on the object: {pddl_object.name}")

            for universal_effect in self.lifted_universal_effects:
                self.logger.debug("Updating the action's signature to temporarily include the quantified parameter.")
                self.action.signature[universal_effect.quantified_parameter] = universal_effect.quantified_type
                if pddl_object.type.name != universal_effect.quantified_type.name:
                    continue

                self.logger.debug(f"Trying to apply the universal effect on the object: {str(pddl_object)}")
                extended_parameter_map = {lifted_param: grounded_object
                                          for lifted_param, grounded_object in
                                          zip(self.action.signature, self.grounded_call_objects)}
                extended_parameter_map[universal_effect.quantified_parameter] = pddl_object.name
                for conditional_effect in universal_effect.conditional_effects:
                    grounded_conditional_effect = GroundedEffect(
                        lifted_antecedents=conditional_effect.antecedents,
                        lifted_discrete_effects=conditional_effect.discrete_effects,
                        lifted_numeric_effects=conditional_effect.numeric_effects,
                        domain=self.domain,
                        action=self.action)
                    grounded_conditional_effect.ground_conditional_effect(extended_parameter_map)
                    if grounded_conditional_effect.antecedents_hold(previous_state):
                        self.logger.debug("The antecedents of the universal effect hold.")
                        grounded_conditional_effect.apply(current_state)

                self.logger.debug("Removing the temporarily added signature item from the action.")
                self.action.signature.pop(universal_effect.quantified_parameter)

    def is_applicable(self, state: State) -> bool:
        """Checks if the action is applicable on the current state.

        :param state: the state prior to the action's execution.
        :return: whether the action is applicable.
        """
        if not self.grounded:
            self.ground()

        return self.grounded_preconditions.is_applicable(state, self.problem_objects)

    def apply(self, previous_state: State, allow_inapplicable_actions: bool = False) -> State:
        """Applies an action on a state and changes the state according to the action's effects.

        :param previous_state: the state in which the operator is being applied on.
        :param allow_inapplicable_actions: whether to allow inapplicable actions to be applied.
        :return: the new state that was created by applying the operator.
        """
        # First need to apply the operator's discrete effects.
        if not self.grounded:
            self.ground()

        if not self.is_applicable(previous_state):
            self.logger.warning("Tried to apply an action to a state where the action's preconditions don't hold!")
            if not allow_inapplicable_actions:
                raise ValueError("Cannot apply an action when it is not applicable!")

        self.logger.debug(f"Applying the grounded action - {self.name} on the current state.")
        new_state = previous_state.copy()
        new_state.is_init = False

        for effect in self.grounded_effects:
            self.logger.debug(f"Applying the effect: {str(effect)}")
            if not effect.antecedents_hold(previous_state):
                self.logger.debug("The antecedents for the effect do not hold so skipping the effect.")
                continue

            effect.apply(new_state)

        self._apply_universal_effects(previous_state, new_state)
        return new_state

    def ground(self) -> None:
        """grounds the operator's preconditions and effects."""
        # First matching the lifted action signature to the grounded objects.
        parameters_map = {lifted_param: grounded_object
                          for lifted_param, grounded_object in zip(self.action.signature, self.grounded_call_objects)}

        self.grounded_preconditions = GroundedPrecondition(
            lifted_precondition=self.action.preconditions, domain=self.domain, action=self.action)
        self.grounded_preconditions.ground_preconditions(parameters_map)
        self.grounded_effects = self._ground_conditional_effects(parameters_map)
        self.grounded = True


class NOPOperator:
    """A no-op operator for when agents do not take action in a certain timestamp."""

    def __str__(self):
        return "(nop )"

    @property
    def name(self):
        return "nop"
