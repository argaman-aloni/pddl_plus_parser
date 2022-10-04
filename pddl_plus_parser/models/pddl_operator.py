"""module to represent an operator that can apply actions and change state objects."""
import logging
from collections import defaultdict
from typing import List, Set, Dict, NoReturn, Tuple, Optional

from anytree import AnyNode

from .conditional_effect import ConditionalEffect
from .numerical_expression import NumericalExpressionTree, evaluate_expression
from .pddl_action import Action
from .pddl_domain import Domain
from .pddl_function import PDDLFunction
from .pddl_predicate import GroundedPredicate, Predicate, SignatureType
from .pddl_state import State


def set_expression_value(expression_node: AnyNode, state_fluents: Dict[str, PDDLFunction]) -> NoReturn:
    """Set the value of the expression according to the fluents present in the state.

    :param expression_node: the node that is currently being observed.
    :param state_fluents: the grounded numeric fluents present in the state.
    """
    if expression_node.is_leaf:
        if not isinstance(expression_node.value, PDDLFunction):
            return

        grounded_fluent: PDDLFunction = expression_node.value
        try:
            grounded_fluent.set_value(state_fluents[grounded_fluent.untyped_representation].value)

        except KeyError:
            grounded_fluent.set_value(0.0)

        return

    set_expression_value(expression_node.children[0], state_fluents)
    set_expression_value(expression_node.children[1], state_fluents)


class Operator:
    action: Action
    domain: Domain
    grounded_call_objects: List[str]
    grounded: bool
    logger: logging.Logger

    # These fields are constructed after the grounding process.
    grounded_positive_preconditions: Set[GroundedPredicate]
    grounded_negative_preconditions: Set[GroundedPredicate]
    grounded_equality_preconditions: Set[Tuple[str, str]]
    grounded_inequality_preconditions: Set[Tuple[str, str]]
    grounded_numeric_preconditions: Set[NumericalExpressionTree]
    grounded_add_effects: Set[GroundedPredicate]
    grounded_delete_effects: Set[GroundedPredicate]
    grounded_numeric_effects: Set[NumericalExpressionTree]
    grounded_conditional_effects: Set[ConditionalEffect]
    grounded_disjunctive_numeric_preconditions: List[Set[NumericalExpressionTree]]

    def __init__(self, action: Action, domain: Domain, grounded_action_call: List[str]):
        self.action = action
        self.domain = domain
        self.grounded_call_objects = grounded_action_call
        self.grounded = False
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

    def ground_predicates(self, lifted_predicates: Set[Predicate],
                          parameters_map: Dict[str, str]) -> Set[GroundedPredicate]:
        """Grounds predicates that appear in the grounded operator.

        :param lifted_predicates: the lifted predicates definition originating from the domain.
        :param parameters_map: the mapping between the action's parameters and the objects that the action
            was actually called with.
        :return: the predicates that appear in the action containing concrete objects.
        """
        output_grounded_predicates = set()
        for predicate in lifted_predicates:
            predicate_name = predicate.name
            # I want the grounded predicate to have the same signature as the original signature so that I can later
            # on efficiently search for it in the states.
            predicate_signature = {param: param_type for param, param_type in
                                   self.domain.predicates[predicate_name].signature.items()}
            predicate_params = list(predicate.signature.keys())
            if len(self.domain.constants) > 0:
                predicate_params.extend(list(self.domain.constants.keys()))

            lifted_predicate_params = [param for param in predicate.signature]
            predicate_object_mapping = {}
            for index, parameter_name in enumerate(predicate_signature):
                if predicate_params[index] in self.domain.constants:
                    predicate_object_mapping[parameter_name] = predicate_params[index]

                else:
                    predicate_object_mapping[parameter_name] = parameters_map[predicate_params[index]]

            # Matching the types to be the same as the ones in the action.
            self._fix_grounded_predicate_types(lifted_predicate_params, predicate_signature)

            output_grounded_predicates.add(GroundedPredicate(name=predicate_name,
                                                             signature=predicate_signature,
                                                             object_mapping=predicate_object_mapping))
        return output_grounded_predicates

    def _fix_grounded_predicate_types(self, lifted_predicate_params: List[str],
                                      predicate_signature: SignatureType) -> NoReturn:
        """Fix the types of the grounded predicate to match those in the action itself.

        :param lifted_predicate_params: the names of the lifted predicate parameters.
        :param predicate_signature: the signature of the grounded predicate.
        """
        for domain_def_parameter, lifted_predicate_param_name in zip(predicate_signature, lifted_predicate_params):
            if lifted_predicate_param_name in self.domain.constants:
                predicate_signature[domain_def_parameter] = self.domain.constants[lifted_predicate_param_name].type

            else:
                predicate_signature[domain_def_parameter] = self.action.signature[lifted_predicate_param_name]

    def iterate_calc_tree_and_ground(self, calc_node: AnyNode, parameters_map: Dict[str, str]) -> AnyNode:
        """Recursion function that iterates over the lifted calculation tree and grounds its elements.

        :param calc_node: the current node the recursion currently visits.
        :param parameters_map: the mapping between the action parameters and the objects in which the action was called.
        :return: the node that represents the calculations of the current lifted expression.
        """
        if calc_node.is_leaf:
            if isinstance(calc_node.value, PDDLFunction):
                lifted_function: PDDLFunction = calc_node.value
                lifted_function_params = [param for param in lifted_function.signature]
                grounded_signature = {}
                for index, parameter_name in enumerate(lifted_function_params):
                    if parameter_name in self.domain.constants:
                        grounded_signature[parameter_name] = lifted_function.signature[parameter_name]

                    else:
                        grounded_signature[parameters_map[lifted_function_params[index]]] = \
                            lifted_function.signature[parameter_name]

                grounded_function = PDDLFunction(name=lifted_function.name,
                                                 signature=grounded_signature)
                return AnyNode(id=str(grounded_function), value=grounded_function)

            return AnyNode(id=calc_node.id, value=calc_node.value)

        return AnyNode(
            id=calc_node.id, value=calc_node.value, children=[
                self.iterate_calc_tree_and_ground(calc_node.children[0], parameters_map),
                self.iterate_calc_tree_and_ground(calc_node.children[1], parameters_map),
            ])

    def ground_numeric_calculation_tree(self, lifted_numeric_exp_tree: NumericalExpressionTree,
                                        parameters_map: Dict[str, str]) -> NumericalExpressionTree:
        """grounds a calculation expression and returns the version containing the objects instead of the parameters.

        :param lifted_numeric_exp_tree: the lifted calculation tree.
        :param parameters_map: the mapping between the action's parameters and the objects in which the action
            was called with.
        :return: the grounded expression tree.
        """
        root = lifted_numeric_exp_tree.root
        grounded_root = self.iterate_calc_tree_and_ground(root, parameters_map)
        return NumericalExpressionTree(expression_tree=grounded_root)

    def ground_numeric_expressions(self, lifted_numeric_exp_tree: Set[NumericalExpressionTree],
                                   parameters_map: Dict[str, str]) -> Set[NumericalExpressionTree]:
        """Grounds a set of numeric expressions.

        :param lifted_numeric_exp_tree: the set containing the numeric expressions to ground.
        :param parameters_map: the mapping between the action's parameters and the objects using which the action was
            called.
        :return: a set containing the grounded expressions.
        """
        grounded_numeric_expressions = set()
        for expression in lifted_numeric_exp_tree:
            grounded_numeric_expressions.add(self.ground_numeric_calculation_tree(expression, parameters_map))

        return grounded_numeric_expressions

    def ground_conditional_effect(self, lifted_condition: ConditionalEffect,
                                  parameters_map: Dict[str, str]) -> ConditionalEffect:
        """Grounds a single conditional effect.

        :param lifted_condition: the conditional effect to ground.
        :param parameters_map: the mapping between the action's parameters and the objects using which the action was
            called.
        :return: a grounded conditional effect.
        """
        grounded_conditional_effect = ConditionalEffect()
        grounded_conditional_effect.positive_conditions = self.ground_predicates(
            lifted_condition.positive_conditions, parameters_map)
        grounded_conditional_effect.negative_conditions = self.ground_predicates(lifted_condition.negative_conditions,
                                                                                 parameters_map)
        grounded_conditional_effect.numeric_conditions = self.ground_numeric_expressions(
            lifted_condition.numeric_conditions, parameters_map)
        grounded_conditional_effect.add_effects = self.ground_predicates(lifted_condition.add_effects, parameters_map)
        grounded_conditional_effect.delete_effects = self.ground_predicates(lifted_condition.delete_effects,
                                                                            parameters_map)
        grounded_conditional_effect.numeric_effects = self.ground_numeric_expressions(lifted_condition.numeric_effects,
                                                                                      parameters_map)
        return grounded_conditional_effect

    @staticmethod
    def ground_equality_objects(equality_preconditions: Set[Tuple[str, str]],
                                parameters_map: Dict[str, str]) -> Set[Tuple[str, str]]:
        """Grounds the in/equality operators from the preconditions.

        :param equality_preconditions: the set of lifted signature items that are to be tested for equality.
        :param parameters_map: the mapping between the lifted and the grounded objects.
        :return: the grounded objects that should/n't be equal.
        """
        return {(parameters_map[obj1], parameters_map[obj2]) for obj1, obj2 in equality_preconditions}

    def ground(self) -> NoReturn:
        """grounds the operator's preconditions and effects."""
        # First matching the lifted action signature to the grounded objects.
        parameters_map = {lifted_param: grounded_object
                          for lifted_param, grounded_object in zip(self.action.signature, self.grounded_call_objects)}

        self.grounded_positive_preconditions = self.ground_predicates(self.action.positive_preconditions,
                                                                      parameters_map)
        self.grounded_negative_preconditions = self.ground_predicates(self.action.negative_preconditions,
                                                                      parameters_map)
        self.grounded_add_effects = self.ground_predicates(self.action.add_effects, parameters_map)
        self.grounded_delete_effects = self.ground_predicates(self.action.delete_effects, parameters_map)
        self.grounded_equality_preconditions = self.ground_equality_objects(self.action.equality_preconditions,
                                                                            parameters_map)
        self.grounded_inequality_preconditions = self.ground_equality_objects(self.action.inequality_preconditions,
                                                                              parameters_map)

        self.grounded_numeric_preconditions = self.ground_numeric_expressions(self.action.numeric_preconditions,
                                                                              parameters_map)
        self.grounded_disjunctive_numeric_preconditions = [
            self.ground_numeric_expressions(expressions, parameters_map) for expressions in
            self.action.disjunctive_numeric_preconditions]
        self.grounded_numeric_effects = self.ground_numeric_expressions(self.action.numeric_effects, parameters_map)
        self.grounded_conditional_effects = {self.ground_conditional_effect(condition, parameters_map) for condition in
                                             self.action.conditional_effects}
        self.grounded = True

    def _positive_preconditions_hold(self, state: State, conditions: Optional[Set[GroundedPredicate]] = None) -> bool:
        """Check whether the positive preconditions hold in the given state.

        :param state: the state which the action is applied on.
        :param conditions: the positive preconditions to check.
        :return: whether the positive preconditions hold.
        """
        positive_conditions = conditions or self.grounded_positive_preconditions
        self.logger.info(
            "Validating whether or not the positive state variables match the operator's grounded predicates.")
        for positive_precondition in positive_conditions:
            try:
                state_grounded_predicates = state.state_predicates[positive_precondition.lifted_untyped_representation]
                untyped_predicates = [p.untyped_representation for p in state_grounded_predicates]
                if not positive_precondition.untyped_representation in untyped_predicates:
                    self.logger.debug(f"Did not find the grounded predicate "
                                      f"{positive_precondition.untyped_representation}")
                    return False

            except KeyError:
                self.logger.debug(f"Did not find the predicate {positive_precondition.lifted_untyped_representation}")
                return False

        self.logger.debug("All positive preconditions we found in the state.")
        return True

    def _negative_preconditions_hold(self, state: State, conditions: Optional[Set[GroundedPredicate]] = None) -> bool:
        """Check whether the negative preconditions hold in the given state.

        :param state: the state which the action is applied on.
        :param conditions: the negative preconditions to check.
        :return: whether the negative preconditions hold.
        """
        negative_conditions = conditions or self.grounded_negative_preconditions
        self.logger.info("Validating that all of the negative preconditions don't exist in the state.")
        for negative_precondition in negative_conditions:
            try:
                state_grounded_predicates = state.state_predicates[negative_precondition.lifted_typed_representation]
                if negative_precondition in state_grounded_predicates:
                    self.logger.debug(
                        f"Found the predicate {str(negative_precondition)} but it should not hold in the state!")
                    return False

            except KeyError:
                continue

        self.logger.debug("All negative preconditions do not hold in the state.")
        return True

    @staticmethod
    def _equality_holds(grounded_objects: Set[Tuple[str, str]]) -> bool:
        """validates if all the requested objects are equal.

        :param grounded_objects: the objects that are being tested.
        :return: whether they are equal.
        """
        return all([obj[0] == obj[1] for obj in grounded_objects])

    def _numeric_conditions_set_hold(self, state: State, numeric_conditions: Set[NumericalExpressionTree]) -> bool:
        """Check if the set of numeric conditions holds as a whole.

        :param state: the state that the action is being applied to.
        :param numeric_conditions: the set of numeric conditions to check.
        :return: whether the set of numeric conditions holds.
        """
        for grounded_expression in numeric_conditions:
            try:
                self.logger.debug("Setting the values of the numeric state functions to the grounded operator")
                set_expression_value(grounded_expression.root, state.state_fluents)
                if not evaluate_expression(grounded_expression.root):
                    self.logger.debug(f"The evaluation of the numeric state variable failed. "
                                      f"The failed expression:\n{str(grounded_expression)}")
                    return False

            except KeyError:
                return False

        return True

    def is_applicable(self, state: State) -> bool:
        """Checks if the action is applicable on the current state.

        :param state: the state prior to the action's execution.
        :return: whether the action is applicable.
        """
        if not self.grounded:
            self.ground()

        if not self._positive_preconditions_hold(state) or not self._negative_preconditions_hold(state):
            return False

        # Checking for objects equality.
        if len(self.grounded_equality_preconditions) > 0 and \
                not self._equality_holds(self.grounded_equality_preconditions) or \
                len(self.grounded_inequality_preconditions) > 0 and \
                self._equality_holds(self.grounded_inequality_preconditions):
            return False

        # Checking that the value of the numeric expression holds.
        if not self._numeric_conditions_set_hold(state, self.grounded_numeric_preconditions):
            return False

        if len(self.grounded_disjunctive_numeric_preconditions) > 0 and \
                not any([self._numeric_conditions_set_hold(state, disjunctive_numeric_preconditions)
                         for disjunctive_numeric_preconditions in self.grounded_disjunctive_numeric_preconditions]):
            self.logger.debug("None of the disjunctive numeric preconditions hold.")
            return False

        return True

    @staticmethod
    def _group_effect_predicates(grounded_effects: Set[GroundedPredicate]) -> Dict[str, Set[GroundedPredicate]]:
        """

        :param grounded_effects:
        :return:
        """
        grouped_effects = defaultdict(set)
        for predicate in grounded_effects:
            grouped_effects[predicate.lifted_untyped_representation].add(predicate)

        return grouped_effects

    @staticmethod
    def _update_single_numeric_expression(numeric_expression: NumericalExpressionTree,
                                          previous_values: Dict[str, PDDLFunction]) -> NoReturn:
        """Updates the numeric value of a single numeric expression.

        :param numeric_expression: the expression that represents the change to the state.
        :param previous_values: the previous values of the numeric expressions in the state.
        """
        set_expression_value(numeric_expression.root, previous_values)
        new_grounded_function = evaluate_expression(numeric_expression.root)
        previous_values[new_grounded_function.untyped_representation] = new_grounded_function

    def update_state_predicates(self, previous_state: State) -> Dict[str, Set[GroundedPredicate]]:
        """Updates the state predicates based on the action that is being applied.

        :param previous_state: the state that the action is being applied on.
        :return: a set of predicates representing the next state.
        """
        self.logger.info("Applying the action on the state predicates.")
        next_state_predicates = {}
        for lifted_predicate_name, grounded_predicates in previous_state.state_predicates.items():
            next_state_predicates[lifted_predicate_name] = \
                set([GroundedPredicate(p.name, p.signature, p.object_mapping) for p in grounded_predicates])

        grouped_delete_effects = self._group_effect_predicates(self.grounded_delete_effects)
        self.logger.debug("Removing state predicates according to the delete effects.")
        for lifted_predicate_str, grounded_predicates in grouped_delete_effects.items():
            next_state_grounded_predicates = next_state_predicates.get(lifted_predicate_str, set())
            if len(next_state_grounded_predicates) == 0:
                next_state_predicates[lifted_predicate_str] = next_state_grounded_predicates
                continue

            for predicate_to_remove in grounded_predicates:
                for next_state_predicate in next_state_grounded_predicates:
                    if predicate_to_remove == next_state_predicate:
                        next_state_grounded_predicates.discard(next_state_predicate)
                        break

            next_state_predicates[lifted_predicate_str] = next_state_grounded_predicates

        grouped_add_effects = self._group_effect_predicates(self.grounded_add_effects)
        self.logger.debug("Adding the new predicates according to the add effects.")
        for lifted_predicate_str, grounded_predicates in grouped_add_effects.items():
            updated_predicates = next_state_predicates.get(lifted_predicate_str, set()).union(grounded_predicates)
            next_state_predicates[lifted_predicate_str] = updated_predicates

        self.logger.debug("Applying the conditional discrete effects!")
        self.update_discrete_conditional_effects(previous_state, next_state_predicates)

        return next_state_predicates

    def update_discrete_conditional_effects(
            self, previous_state: State, next_state_predicates: Dict[str, Set[GroundedPredicate]]):
        """Checks whether the conditions for the conditional effects hold and updates the discrete state accordingly.

        :param previous_state: the state that the action is being applied on.
        :param next_state_predicates: the next state predicates.
        """
        for effect in self.grounded_conditional_effects:
            if not (self._positive_preconditions_hold(previous_state, effect.positive_conditions)
                    and self._negative_preconditions_hold(previous_state, effect.negative_conditions) and
                    self._numeric_conditions_set_hold(previous_state, effect.numeric_conditions)):
                continue

            self.logger.debug("The conditionals for the effect hold so applying the effect.")
            for predicate in effect.add_effects:
                lifted_predicate_str = predicate.lifted_untyped_representation
                next_state_grounded_predicates = next_state_predicates.get(lifted_predicate_str, set())
                next_state_grounded_predicates.add(predicate)
                next_state_predicates[lifted_predicate_str] = next_state_grounded_predicates

            for predicate in effect.delete_effects:
                next_state_predicates[predicate.lifted_untyped_representation].discard(predicate)

    def update_numeric_conditional_effects(
            self, previous_state: State, new_state_numeric_fluents: Dict[str, PDDLFunction]) -> NoReturn:
        """Checks whether the conditions for the conditional effects hold and updates the discrete state accordingly.

        :param previous_state: the state that the action is being applied on.
        :param new_state_numeric_fluents: the next state grounded numeric functions.
        """
        for effect in self.grounded_conditional_effects:
            if not (self._positive_preconditions_hold(previous_state, effect.positive_conditions)
                    and self._negative_preconditions_hold(previous_state, effect.negative_conditions) and
                    self._numeric_conditions_set_hold(previous_state, effect.numeric_conditions)):
                continue

            self.logger.debug("The conditionals for the effect hold so applying the numeric effect.")
            for grounded_expression in effect.numeric_effects:
                self._update_single_numeric_expression(grounded_expression, new_state_numeric_fluents)

    def update_state_functions(self, previous_state: State) -> Dict[str, PDDLFunction]:
        """Updates the state functions based on the action that is being applied.

        :param previous_state: the state that the action is being applied on.
        :return: the updated state functions with their new values.
        """
        new_state_numeric_fluents = {**previous_state.state_fluents}
        for grounded_expression in self.grounded_numeric_effects:
            try:
                self.logger.debug("First setting the values of the functions according to the stored state.")
                self._update_single_numeric_expression(grounded_expression, new_state_numeric_fluents)

            except KeyError:
                raise ValueError(f"There are missing fluents in the state! "
                                 f"State fluents: {previous_state.state_fluents}\n"
                                 f"Requested grounded expression:\n {str(grounded_expression)}")

        return new_state_numeric_fluents

    def apply(self, previous_state: State) -> State:
        """Applies an action on a state and changes the state according to the action's effects.

        :param previous_state: the state in which the operator is being applied on.
        :return: the new state that was created by applying the operator.
        """
        # First need to apply the operator's discrete effects.
        if not self.grounded:
            self.ground()

        if not self.is_applicable(previous_state):
            self.logger.warning("Tried to apply an action to a state where the action's preconditions don't hold!")
            raise ValueError()

        self.logger.debug(f"Applying the grounded action - {self.name} on the current state.")
        next_state_predicates = self.update_state_predicates(previous_state)
        next_state_numeric_fluents = self.update_state_functions(previous_state)
        return State(predicates=next_state_predicates, fluents=next_state_numeric_fluents)


class NOPOperator:
    """A no-op operator for when agents do not take action in a certain timestamp."""

    def __str__(self):
        return "(nop )"

    @property
    def name(self):
        return "nop"
