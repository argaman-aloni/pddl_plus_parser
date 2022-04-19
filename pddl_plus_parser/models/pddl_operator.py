"""module to represent an operator that can apply actions and change state objects."""
import logging
from collections import defaultdict
from typing import List, Set, Dict, NoReturn

from anytree import AnyNode

from . import PDDLFunction
from .numerical_expression import NumericalExpressionTree, evaluate_expression
from .pddl_action import Action
from .pddl_domain import Domain
from .pddl_predicate import GroundedPredicate, Predicate
from .pddl_state import State


def set_expression_value(expression_node: AnyNode, state_fluents: Dict[str, PDDLFunction]) -> NoReturn:
    """Set the value of the expression according to the fluents present in the state.

    :param expression_node: the node that is currently being observed.
    """
    if expression_node.is_leaf:
        if not isinstance(expression_node.value, PDDLFunction):
            return

        grounded_fluent: PDDLFunction = expression_node.value
        grounded_fluent.set_value(state_fluents[grounded_fluent.untyped_representation].value)
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
    grounded_numeric_preconditions: Set[NumericalExpressionTree]
    grounded_add_effects: Set[GroundedPredicate]
    grounded_delete_effects: Set[GroundedPredicate]
    grounded_numeric_effects: Set[NumericalExpressionTree]

    def __init__(self, action: Action, domain: Domain, grounded_action_call: List[str]):
        self.action = action
        self.domain = domain
        self.grounded_call_objects = grounded_action_call
        self.grounded = False
        self.logger = logging.getLogger(__name__)

    @property
    def name(self) -> str:
        return self.action.name

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
            lifted_predicate_params = [param for param in predicate.signature]
            predicate_object_mapping = {
                parameter_name: parameters_map[lifted_predicate_params[index]] for index, parameter_name in
                enumerate(predicate_signature)}

            # Matching the types to be the same as the ones in the action.
            for domain_def_parameter, lifted_predicate_param_name in zip(predicate_signature, lifted_predicate_params):
                predicate_signature[domain_def_parameter] = self.action.signature[lifted_predicate_param_name]

            output_grounded_predicates.add(GroundedPredicate(name=predicate_name,
                                                             signature=predicate_signature,
                                                             object_mapping=predicate_object_mapping))
        return output_grounded_predicates

    def iterate_calc_tree_and_ground(self, calc_node: AnyNode, parameters_map: Dict[str, str]) -> AnyNode:
        """Recursion function that iterates over the lifted calculation tree and grounds its elements.

        :param calc_tree: the current node the recursion currently visits.
        :param parameters_map: the mapping between the action parameters and the objects in which the action was called.
        :return: the node that represents the calculations of the current lifted expression.
        """
        if calc_node.is_leaf:
            if isinstance(calc_node.value, PDDLFunction):
                lifted_function: PDDLFunction = calc_node.value
                lifted_function_params = [param for param in lifted_function.signature]
                grounded_signature = {
                    parameters_map[lifted_function_params[index]]: lifted_function.signature[parameter_name] for
                    index, parameter_name in enumerate(lifted_function_params)}
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

        self.grounded_numeric_preconditions = self.ground_numeric_expressions(self.action.numeric_preconditions,
                                                                              parameters_map)
        self.grounded_numeric_effects = self.ground_numeric_expressions(self.action.numeric_effects, parameters_map)
        self.grounded = True

    def _positive_preconditions_hold(self, state: State) -> bool:
        """

        :param state:
        :return:
        """
        self.logger.info(
            "Validating whether or not the positive state variables match the operator's grounded predicates.")
        for positive_precondition in self.grounded_positive_preconditions:
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

    def _negative_preconditions_hold(self, state: State) -> bool:
        """

        :param state:
        :return:
        """
        self.logger.info("Validating that all of the negative preconditions don't exist in the state.")
        for negative_precondition in self.grounded_negative_preconditions:
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

    def is_applicable(self, state: State) -> bool:
        """Checks if the action is applicable on the current state.

        :param state: the state prior to the action's execution.
        :return: whether or not the action is applicable.
        """
        if not self.grounded:
            self.ground()

        if not self._positive_preconditions_hold(state) or not self._negative_preconditions_hold(state):
            return False

        # Checking that the value of the numeric expression holds.
        for grounded_expression in self.grounded_numeric_preconditions:
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

    def _group_effect_predicates(self, grounded_effects: Set[GroundedPredicate]) -> Dict[str, Set[GroundedPredicate]]:
        """

        :param grounded_effects:
        :return:
        """
        grouped_effects = defaultdict(set)
        for predicate in grounded_effects:
            grouped_effects[predicate.lifted_untyped_representation].add(predicate)

        return grouped_effects

    def update_state_predicates(self, previous_state: State) -> Dict[str, Set[GroundedPredicate]]:
        """Updates the state predicates based on the action that is being applied.

        :param previous_state: the state that the action is being applied on.
        :return: a set of predicates representing the next state.
        """
        self.logger.info("Applying the action on the state predicates.")
        next_state_predicates = {}
        for lifted_predicate_name, grounded_predicates in previous_state.state_predicates.items():
            next_state_predicates[lifted_predicate_name] =\
                set([GroundedPredicate(p.name, p.signature, p.object_mapping) for p in grounded_predicates])

        grouped_add_effects = self._group_effect_predicates(self.grounded_add_effects)
        self.logger.debug("Adding the new predicates according to the add effects.")
        for lifted_predicate_str, grounded_predicates in grouped_add_effects.items():
            updated_predicates = next_state_predicates.get(lifted_predicate_str, set()).union(grounded_predicates)
            next_state_predicates[lifted_predicate_str] = updated_predicates

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

        return next_state_predicates

    def update_state_functions(self, previous_state: State) -> Dict[str, PDDLFunction]:
        """

        :param previous_state:
        :return:
        """
        new_state_numeric_fluents = {**previous_state.state_fluents}
        for grounded_expression in self.grounded_numeric_effects:
            try:
                self.logger.debug("First setting the values of the functions according to the stored state.")
                set_expression_value(grounded_expression.root, previous_state.state_fluents)
                new_grounded_function = evaluate_expression(grounded_expression.root)
                new_state_numeric_fluents[new_grounded_function.untyped_representation] = new_grounded_function

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
