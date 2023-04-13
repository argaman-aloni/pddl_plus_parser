"""module to represent an operator that can apply actions and change state objects."""
import logging
from collections import defaultdict
from typing import List, Set, Dict, Tuple, Optional, Union

from anytree import AnyNode

from .conditional_effect import ConditionalEffect, UniversalEffect
from .numerical_expression import NumericalExpressionTree, evaluate_expression
from .pddl_action import Action
from .pddl_domain import Domain
from .pddl_function import PDDLFunction
from .pddl_object import PDDLObject
from .pddl_precondition import CompoundPrecondition, Precondition, UniversalPrecondition
from .pddl_predicate import GroundedPredicate, Predicate, SignatureType
from .pddl_state import State

BinaryOperator = {
    "and": lambda x, y: x and y,
    "or": lambda x, y: x or y
}


def set_expression_value(expression_node: AnyNode, state_fluents: Dict[str, PDDLFunction]) -> None:
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


def fix_grounded_predicate_types(lifted_predicate_params: List[str],
                                 predicate_signature: SignatureType, domain: Domain, action: Action) -> None:
    """Fix the types of the grounded predicate to match those in the action itself.

    :param lifted_predicate_params: the names of the lifted predicate parameters.
    :param predicate_signature: the signature of the grounded predicate.
    """
    for domain_def_parameter, lifted_predicate_param_name in zip(predicate_signature, lifted_predicate_params):
        if lifted_predicate_param_name in domain.constants:
            predicate_signature[domain_def_parameter] = domain.constants[lifted_predicate_param_name].type

        else:
            predicate_signature[domain_def_parameter] = action.signature[lifted_predicate_param_name]


def ground_predicate(predicate: Predicate, parameters_map: Dict[str, str],
                     domain: Domain, action: Action) -> GroundedPredicate:
    """Ground a predicate.

    :param predicate: the predicate to ground.
    :param parameters_map: the mapping of parameters to objects.
    :return: the grounded predicate.
    """
    predicate_name = predicate.name
    # I want the grounded predicate to have the same signature as the original signature so that I can later
    # on efficiently search for it in the states.
    predicate_signature = {param: param_type for param, param_type in
                           domain.predicates[predicate_name].signature.items()}
    predicate_params = list(predicate.signature.keys())
    if len(domain.constants) > 0:
        predicate_params.extend(list(domain.constants.keys()))

    lifted_predicate_params = [param for param in predicate.signature]
    predicate_object_mapping = {}
    for index, parameter_name in enumerate(predicate_signature):
        if predicate_params[index] in domain.constants:
            predicate_object_mapping[parameter_name] = predicate_params[index]

        else:
            predicate_object_mapping[parameter_name] = parameters_map[predicate_params[index]]

    # Matching the types to be the same as the ones in the action.
    fix_grounded_predicate_types(lifted_predicate_params, predicate_signature, domain, action)

    return GroundedPredicate(name=predicate_name, signature=predicate_signature,
                             object_mapping=predicate_object_mapping, is_positive=predicate.is_positive)


def _iterate_calc_tree_and_ground(calc_node: AnyNode, parameters_map: Dict[str, str], domain: Domain) -> AnyNode:
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
                if parameter_name in domain.constants:
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
            _iterate_calc_tree_and_ground(calc_node.children[0], parameters_map, domain),
            _iterate_calc_tree_and_ground(calc_node.children[1], parameters_map, domain),
        ])


def ground_numeric_calculation_tree(lifted_numeric_exp_tree: NumericalExpressionTree,
                                    parameters_map: Dict[str, str], domain: Domain) -> NumericalExpressionTree:
    """grounds a calculation expression and returns the version containing the objects instead of the parameters.

    :param lifted_numeric_exp_tree: the lifted calculation tree.
    :param parameters_map: the mapping between the action's parameters and the objects in which the action
        was called with.
    :return: the grounded expression tree.
    """
    root = lifted_numeric_exp_tree.root
    grounded_root = _iterate_calc_tree_and_ground(root, parameters_map, domain)
    return NumericalExpressionTree(expression_tree=grounded_root)


def ground_numeric_expressions(lifted_numeric_exp_tree: Set[NumericalExpressionTree],
                               parameters_map: Dict[str, str], domain: Domain) -> Set[NumericalExpressionTree]:
    """Grounds a set of numeric expressions.

    :param lifted_numeric_exp_tree: the set containing the numeric expressions to ground.
    :param parameters_map: the mapping between the action's parameters and the objects using which the action was
        called.
    :return: a set containing the grounded expressions.
    """
    grounded_numeric_expressions = set()
    for expression in lifted_numeric_exp_tree:
        grounded_numeric_expressions.add(ground_numeric_calculation_tree(expression, parameters_map, domain))

    return grounded_numeric_expressions


class GroundedPrecondition:
    """class representing the grounded version of an action's precondition."""
    _lifted_precondition: CompoundPrecondition
    _grounded_precondition: CompoundPrecondition
    logger: logging.Logger

    def __init__(self, lifted_precondition: CompoundPrecondition, domain: Domain, action: Action):
        self._lifted_precondition = lifted_precondition
        self._grounded_precondition = CompoundPrecondition()
        self.domain = domain
        self.action = action
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _ground_equality_objects(equality_preconditions: Set[Tuple[str, str]],
                                 parameters_map: Dict[str, str]) -> Set[Tuple[str, str]]:
        """Grounds the in/equality operators from the preconditions.

        :param equality_preconditions: the set of lifted signature items that are to be tested for equality.
        :param parameters_map: the mapping between the lifted and the grounded objects.
        :return: the grounded objects that should/n't be equal.
        """
        return {(parameters_map[obj1], parameters_map[obj2]) for obj1, obj2 in equality_preconditions}

    def _ground(self, lifted_conditions: Precondition, grounded_conditions: Precondition,
                parameters_map: Dict[str, str]) -> None:
        """Ground the preconditions of the action."""
        for precondition in lifted_conditions.operands:
            if isinstance(precondition, Predicate):
                grounded_predicate = ground_predicate(precondition, parameters_map, self.domain, self.action)
                grounded_conditions.add_condition(grounded_predicate)

            elif isinstance(precondition, NumericalExpressionTree):
                grounded_conditions.add_condition(ground_numeric_calculation_tree(
                    precondition, parameters_map, self.domain))

            elif isinstance(precondition, UniversalPrecondition):
                self.logger.debug("Currently not supporting universal preconditions.")
                continue

            elif isinstance(precondition, Precondition):
                grounded_condition = Precondition(precondition.binary_operator)
                grounded_condition.equality_preconditions = \
                    self._ground_equality_objects(precondition.equality_preconditions, parameters_map)
                grounded_condition.inequality_preconditions = self._ground_equality_objects(
                    precondition.inequality_preconditions, parameters_map)
                self._ground(precondition, grounded_condition, parameters_map)

            else:
                raise ValueError(f"Unknown precondition type: {type(lifted_conditions)}")

    def ground_preconditions(self, parameters_map: Dict[str, str]) -> None:
        """Ground the preconditions of the action.

        :param state: the state to ground the preconditions in.
        """
        self._grounded_precondition.root.equality_preconditions = \
            self._ground_equality_objects(self._lifted_precondition.root.equality_preconditions, parameters_map)
        self._grounded_precondition.root.inequality_preconditions = self._ground_equality_objects(
            self._lifted_precondition.root.inequality_preconditions, parameters_map)

        self._ground(lifted_conditions=self._lifted_precondition.root,
                     grounded_conditions=self._grounded_precondition.root, parameters_map=parameters_map)

    def _is_condition_applicable(self, preconditions: Union[GroundedPredicate, NumericalExpressionTree, Precondition],
                                 state: State) -> bool:
        """

        :param preconditions:
        :param state:
        :return:
        """
        is_applicable = True
        for condition in preconditions.operands:
            if isinstance(condition, GroundedPredicate):
                self.logger.debug(f"Validating if the predicate {condition.untyped_representation} "
                                  f"is applicable in the state")
                is_applicable = BinaryOperator[preconditions.binary_operator](
                    is_applicable, condition.untyped_representation in state.serialize() if condition.is_positive else
                    condition.untyped_representation not in state.serialize())

            elif isinstance(condition, NumericalExpressionTree):
                try:
                    set_expression_value(condition.root, state.state_fluents)
                    self.logger.debug(f"Validating if the expression {condition.to_pddl()} is applicable in the state")
                    is_applicable = BinaryOperator[preconditions.binary_operator](
                        is_applicable, evaluate_expression(condition.root))

                except KeyError:
                    is_applicable = False

            elif isinstance(condition, Precondition):
                is_applicable = BinaryOperator[preconditions.binary_operator](
                    is_applicable, self._is_condition_applicable(condition, state))

            else:
                raise ValueError(f"Unknown precondition type: {type(condition)}")

        return is_applicable

    def is_applicable(self, state: State) -> bool:
        """Check whether the precondition is satisfied in the given state.

        :param state: the state to check.
        :return: True if the precondition is satisfied, False otherwise.
        """
        self.logger.debug(f"Validating if the preconditions hold in the state.")
        return self._is_condition_applicable(self._grounded_precondition.root, state)


class GroundedConditionalEffect:
    grounded_antecedents: GroundedPrecondition
    _lifted_discrete_effects: Set[Predicate]
    _lifted_numeric_effects: Set[NumericalExpressionTree]
    grounded_discrete_effects: Set[GroundedPredicate]
    grounded_numeric_effects: Set[NumericalExpressionTree]

    def __init__(self, lifted_antecedents: CompoundPrecondition,
                 lifted_discrete_effects: Set[Predicate], lifted_numeric_effects: Set[NumericalExpressionTree],
                 domain: Domain, action: Action):
        self.grounded_antecedents = GroundedPrecondition(lifted_antecedents, domain, action)
        self._lifted_discrete_effects = lifted_discrete_effects
        self._lifted_numeric_effects = lifted_numeric_effects
        self.domain = domain
        self.action = action
        self.grounded_discrete_effects = set()
        self.grounded_numeric_effects = set()
        self.logger = logging.getLogger(__name__)

    def ground_conditional_effect(self, parameters_map: Dict[str, str]) -> None:
        """

        :param parameters_map:
        :return:
        """
        self.grounded_antecedents.ground_preconditions(parameters_map)
        for effect in self._lifted_discrete_effects:
            self.grounded_discrete_effects.add(ground_predicate(effect, parameters_map, self.domain, self.action))

        for effect in self._lifted_numeric_effects:
            self.grounded_numeric_effects.add(ground_numeric_calculation_tree(effect, parameters_map, self.domain))

    def antecedents_hold(self, state: State) -> bool:
        """

        :param state:
        :return:
        """
        return self.grounded_antecedents.is_applicable(state)


class Operator:
    action: Action
    domain: Domain
    grounded_call_objects: List[str]
    grounded: bool
    logger: logging.Logger

    # These fields are constructed after the grounding process.
    grounded_preconditions: GroundedPrecondition
    grounded_discrete_effects: Set[GroundedPredicate]
    grounded_numeric_effects: Set[NumericalExpressionTree]
    grounded_conditional_effects: Set[GroundedConditionalEffect]
    lifted_universal_effects: Set[UniversalEffect]
    problem_objects: Dict[str, PDDLObject]

    def __init__(self, action: Action, domain: Domain, grounded_action_call: List[str],
                 problem_objects: Optional[Dict[str, PDDLObject]] = None):
        self.action = action
        self.domain = domain
        self.grounded_call_objects = grounded_action_call
        self.grounded = False
        self.problem_objects = problem_objects
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

    def _ground_conditional_effect(self, lifted_condition: ConditionalEffect,
                                   parameters_map: Dict[str, str]) -> GroundedConditionalEffect:
        """Grounds a single conditional effect.

        :param lifted_condition: the conditional effect to ground.
        :param parameters_map: the mapping between the action's parameters and the objects using which the action was
            called.
        :return: a grounded conditional effect.
        """
        grounded_conditional_effect = GroundedConditionalEffect(
            lifted_antecedents=lifted_condition.antecedents, lifted_discrete_effects=lifted_condition.discrete_effects,
            lifted_numeric_effects=lifted_condition.numeric_effects, domain=self.domain, action=self.action)
        grounded_conditional_effect.ground_conditional_effect(parameters_map)
        return grounded_conditional_effect

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
                                          previous_values: Dict[str, PDDLFunction]) -> None:
        """Updates the numeric value of a single numeric expression.

        :param numeric_expression: the expression that represents the change to the state.
        :param previous_values: the previous values of the numeric expressions in the state.
        """
        set_expression_value(numeric_expression.root, previous_values)
        new_grounded_function = evaluate_expression(numeric_expression.root)
        previous_values[new_grounded_function.untyped_representation] = new_grounded_function

    def _update_delete_effects(self, next_state_predicates: Dict[str, Set[GroundedPredicate]]) -> None:
        """Updates the state with the delete effects.

        :param next_state_predicates: the next state predicates.
        """
        grouped_delete_effects = self._group_effect_predicates(
            {predicate for predicate in self.grounded_discrete_effects if not predicate.is_positive})
        self.logger.debug("Removing state predicates according to the delete effects.")
        for lifted_predicate_str, grounded_predicates in grouped_delete_effects.items():
            next_state_grounded_predicates = next_state_predicates[lifted_predicate_str]
            if len(next_state_grounded_predicates) == 0:
                next_state_predicates[lifted_predicate_str] = set()
                continue

            for predicate_to_remove in grounded_predicates:
                for next_state_predicate in next_state_grounded_predicates:
                    if predicate_to_remove.untyped_representation == next_state_predicate.untyped_representation:
                        next_state_grounded_predicates.discard(next_state_predicate)
                        break

            next_state_predicates[lifted_predicate_str] = next_state_grounded_predicates

    def _update_add_effects(self, next_state_predicates: Dict[str, Set[GroundedPredicate]]) -> None:
        """Updates the state with the add effects.

        :param next_state_predicates: the next state predicates.
        """
        grouped_add_effects = self._group_effect_predicates(
            {predicate for predicate in self.grounded_discrete_effects if predicate.is_positive})
        self.logger.debug("Adding the new predicates according to the add effects.")
        for lifted_predicate_str, grounded_predicates in grouped_add_effects.items():
            updated_predicates = next_state_predicates[lifted_predicate_str].union(grounded_predicates)
            next_state_predicates[lifted_predicate_str] = updated_predicates

    def update_state_predicates(self, previous_state: State) -> Dict[str, Set[GroundedPredicate]]:
        """Updates the state predicates based on the action that is being applied.

        :param previous_state: the state that the action is being applied on.
        :return: a set of predicates representing the next state.
        """
        self.logger.info("Applying the action on the state predicates.")
        next_state_predicates = defaultdict(set)
        for lifted_predicate_name, grounded_predicates in previous_state.state_predicates.items():
            next_state_predicates[lifted_predicate_name] = \
                set([GroundedPredicate(p.name, p.signature, p.object_mapping) for p in grounded_predicates])

        self._update_delete_effects(next_state_predicates)
        self._update_add_effects(next_state_predicates)

        self.logger.debug("Applying the conditional discrete effects!")
        self.update_discrete_conditional_effects(previous_state, next_state_predicates,
                                                 self.grounded_conditional_effects)
        self.logger.debug("Applying universal effects on the state!")
        self.update_universal_effects(previous_state, next_state_predicates)

        return next_state_predicates

    def update_universal_effects(
            self, previous_state: State, next_state_predicates: Dict[str, Set[GroundedPredicate]]) -> None:
        """Updates the state predicates based on the universal effects of the action.

        :param previous_state: the state that the action is being applied on.
        :param next_state_predicates: the next state predicates.
        """
        if self.problem_objects is None:
            self.logger.warning("Did not receive the problem object so cannot apply the universal effects.")
            return

        for universal_effect in self.lifted_universal_effects:
            self.logger.debug("Updating the action's signature to temporarily include the quantified parameter.")
            self.action.signature[universal_effect.quantified_parameter] = universal_effect.quantified_type
            for pddl_object in self.problem_objects.values():
                if pddl_object.type.name != universal_effect.quantified_type.name:
                    continue

                self.logger.debug(f"Trying to apply the universal effect on the object: {str(pddl_object)}")
                extended_parameter_map = {lifted_param: grounded_object
                                          for lifted_param, grounded_object in
                                          zip(self.action.signature, self.grounded_call_objects)}
                extended_parameter_map[universal_effect.quantified_parameter] = pddl_object.name
                for conditional_effect in universal_effect.conditional_effects:
                    grounded_conditional_effect = self._ground_conditional_effect(conditional_effect,
                                                                                  extended_parameter_map)
                    self.update_discrete_conditional_effects(previous_state, next_state_predicates,
                                                             {grounded_conditional_effect})

            self.logger.debug("Removing the temporarily added signature item from the action.")
            self.action.signature.pop(universal_effect.quantified_parameter)

    def update_discrete_conditional_effects(
            self, previous_state: State, next_state_predicates: Dict[str, Set[GroundedPredicate]],
            conditional_effects: Set[GroundedConditionalEffect]) -> None:
        """Checks whether the conditions for the conditional effects hold and updates the discrete state accordingly.

        :param previous_state: the state that the action is being applied on.
        :param next_state_predicates: the next state predicates.
        :param conditional_effects: the conditional effects that need to be applied.
        """
        for effect in conditional_effects:
            if not effect.antecedents_hold(state=previous_state):
                self.logger.debug(
                    f"Some of the antecedents for the conditional effect do not hold for the action {self.name}.")
                continue

            self.logger.debug("The antecedents for the effect hold so applying the effect.")
            for predicate in effect.grounded_discrete_effects:
                lifted_predicate_str = predicate.lifted_untyped_representation
                if not predicate.is_positive:
                    next_state_predicates[lifted_predicate_str].discard(predicate)

                else:
                    next_state_grounded_predicates = next_state_predicates.get(lifted_predicate_str, set())
                    next_state_grounded_predicates.add(predicate)
                    next_state_predicates[lifted_predicate_str] = next_state_grounded_predicates

    def update_numeric_conditional_effects(
            self, previous_state: State, new_state_numeric_fluents: Dict[str, PDDLFunction]) -> None:
        """Checks whether the conditions for the conditional effects hold and updates the discrete state accordingly.

        :param previous_state: the state that the action is being applied on.
        :param new_state_numeric_fluents: the next state grounded numeric functions.
        """
        for effect in self.grounded_conditional_effects:
            if not effect.antecedents_hold(previous_state):
                continue

            self.logger.debug("The conditionals for the effect hold so applying the numeric effect.")
            for grounded_expression in effect.grounded_numeric_effects:
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

    def is_applicable(self, state: State) -> bool:
        """Checks if the action is applicable on the current state.

        :param state: the state prior to the action's execution.
        :return: whether the action is applicable.
        """
        if not self.grounded:
            self.ground()

        return self.grounded_preconditions.is_applicable(state)

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
                raise ValueError()

        self.logger.debug(f"Applying the grounded action - {self.name} on the current state.")
        next_state_predicates = self.update_state_predicates(previous_state)
        next_state_numeric_fluents = self.update_state_functions(previous_state)
        self.update_numeric_conditional_effects(previous_state, next_state_numeric_fluents)
        return State(predicates=next_state_predicates, fluents=next_state_numeric_fluents)

    def ground(self) -> None:
        """grounds the operator's preconditions and effects."""
        # First matching the lifted action signature to the grounded objects.
        parameters_map = {lifted_param: grounded_object
                          for lifted_param, grounded_object in zip(self.action.signature, self.grounded_call_objects)}

        self.grounded_preconditions = GroundedPrecondition(
            lifted_precondition=self.action.preconditions, domain=self.domain, action=self.action)
        self.grounded_discrete_effects = {
            ground_predicate(effect, parameters_map, domain=self.domain, action=self.action)
            for effect in self.action.discrete_effects}
        self.grounded_numeric_effects = ground_numeric_expressions(
            self.action.numeric_effects, parameters_map, self.domain)
        self.grounded_conditional_effects = {self._ground_conditional_effect(condition, parameters_map) for condition in
                                             self.action.conditional_effects}
        self.lifted_universal_effects = self.action.universal_effects
        self.grounded = True


class NOPOperator:
    """A no-op operator for when agents do not take action in a certain timestamp."""

    def __str__(self):
        return "(nop )"

    @property
    def name(self):
        return "nop"
