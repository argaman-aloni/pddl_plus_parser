"""Module to encapsulate the functionality of grounded preconditions."""
import logging
from typing import Set, Tuple, Dict, Optional

from pddl_plus_parser.models.grounding_utils import ground_predicate, ground_numeric_calculation_tree
from pddl_plus_parser.models.numerical_expression import NumericalExpressionTree, evaluate_expression, \
    set_expression_value
from pddl_plus_parser.models.pddl_action import Action
from pddl_plus_parser.models.pddl_domain import Domain
from pddl_plus_parser.models.pddl_object import PDDLObject
from pddl_plus_parser.models.pddl_precondition import CompoundPrecondition, Precondition, UniversalPrecondition
from pddl_plus_parser.models.pddl_predicate import Predicate, GroundedPredicate
from pddl_plus_parser.models.pddl_state import State

BinaryOperator = {
    "and": lambda x, y: x and y,
    "or": lambda x, y: x or y
}


class GroundedPrecondition:
    """class representing the grounded version of an action's precondition."""
    _lifted_precondition: CompoundPrecondition
    _grounded_precondition: CompoundPrecondition
    _parameter_map: Dict[str, str]
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
        """Ground the preconditions of the action.

        :param lifted_conditions: the lifted preconditions of the action.
        :param grounded_conditions: the grounded preconditions of the action.
        :param parameters_map: the mapping between the lifted and the grounded objects.
        """
        for precondition in lifted_conditions.operands:
            if isinstance(precondition, Predicate):
                grounded_predicate = ground_predicate(precondition, parameters_map, self.domain, self.action)
                grounded_conditions.add_condition(grounded_predicate)

            elif isinstance(precondition, NumericalExpressionTree):
                grounded_conditions.add_condition(ground_numeric_calculation_tree(
                    precondition, parameters_map, self.domain))

            elif isinstance(precondition, UniversalPrecondition):
                self._parameter_map = parameters_map
                self.logger.debug("There is no need to ground universal preconditions.")
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

    @staticmethod
    def _validate_equality_holds(preconditions: Precondition) -> bool:
        """Validate if the equality preconditions hold.

        :param preconditions: the preconditions to validate.
        :return: whether the equality preconditions hold.
        """
        return all([obj1 == obj2 for obj1, obj2 in preconditions.equality_preconditions]) and \
            all([obj1 != obj2 for obj1, obj2 in preconditions.inequality_preconditions])

    def _validate_numeric_expression_hold(self, condition: NumericalExpressionTree, prev_is_applicable: bool,
                                          preconditions: Precondition, state: State) -> bool:
        """Validate if the given numeric expression is applicable in the given state.
        
        :param condition: the numeric expression to validate.
        :param prev_is_applicable: whether the previous conditions were applicable.
        :param preconditions: the preconditions to validate.
        :param state: the state to validate the numeric expression in.
        :return: whether the numeric expression is applicable in the given state.
        """
        try:
            set_expression_value(condition.root, state.state_fluents)
            self.logger.debug(f"Validating if the expression {condition.to_pddl()} is applicable in the state")
            is_applicable = BinaryOperator[preconditions.binary_operator](
                prev_is_applicable, evaluate_expression(condition.root))

        except KeyError:
            is_applicable = False

        return is_applicable

    def _validate_predicates_hold(self, condition: GroundedPredicate, prev_is_applicable: bool,
                                  preconditions: Precondition, state: State) -> bool:
        """Validate if the given predicate is applicable in the given state.
        
        :param condition: the predicate to validate.
        :param prev_is_applicable: whether the previous conditions were applicable.
        :param preconditions: the preconditions to validate.
        :param state: the state to validate the predicate in.
        :return: whether the predicate is applicable in the given state.
        """
        self.logger.debug(f"Validating if the predicate {condition.untyped_representation} "
                          f"is applicable in the state")
        positive_condition_predicate = condition.copy()
        positive_condition_predicate.is_positive = True

        is_applicable = BinaryOperator[preconditions.binary_operator](
            prev_is_applicable, condition.untyped_representation in state.serialize() if condition.is_positive else
            positive_condition_predicate.untyped_representation not in state.serialize())
        return is_applicable

    def _ground_universal_condition(self, condition: UniversalPrecondition,
                                    extended_parameter_map: Dict[str, str]) -> Precondition:
        """Ground the universal precondition.
        
        :param condition: the universal precondition to ground.
        :param extended_parameter_map: the mapping between the lifted and the grounded objects with the quantified 
            object as well.
        :return: the grounded condition for a single object.
        """
        grounded_preconditions = Precondition(condition.binary_operator)
        tmp_action = Action()
        tmp_action.signature = self.action.signature
        tmp_action.signature[condition.quantified_parameter] = condition.quantified_type
        for sub_condition in condition.operands:
            if isinstance(sub_condition, Predicate):
                grounded_predicate = ground_predicate(sub_condition, extended_parameter_map, self.domain,
                                                      tmp_action)
                grounded_preconditions.add_condition(grounded_predicate)

            elif isinstance(sub_condition, NumericalExpressionTree):
                grounded_preconditions.add_condition(ground_numeric_calculation_tree(
                    sub_condition, extended_parameter_map, self.domain))

        return grounded_preconditions

    def _validate_universal_precondition(self, condition: UniversalPrecondition, state: State,
                                         problem_objects: Optional[Dict[str, PDDLObject]] = None) -> bool:
        """Validate if the given universal precondition is applicable in the given state.

        :param condition: the universal precondition to validate.
        :param state: the state to validate the precondition in.
        :return: whether the universal precondition is applicable in the given state.
        """
        if not problem_objects:
            raise ValueError("The objects of the problem should be provided for universal preconditions.")

        self.logger.debug("Validating if the universal precondition is applicable in the state")
        is_applicable = self._validate_equality_holds(condition)
        self.logger.debug("We assume that universal preconditions are not nested.")
        extended_parameter_map = {**self._parameter_map}
        for obj_name, obj in problem_objects.items():
            if obj.type.name != condition.quantified_type.name:
                continue

            extended_parameter_map[condition.quantified_parameter] = obj_name
            grounded_precondition = self._ground_universal_condition(condition, extended_parameter_map)
            for sub_condition in grounded_precondition.operands:
                if isinstance(sub_condition, GroundedPredicate):
                    is_applicable = self._validate_predicates_hold(sub_condition, is_applicable, condition, state)

                elif isinstance(sub_condition, NumericalExpressionTree):
                    is_applicable = self._validate_numeric_expression_hold(sub_condition, is_applicable, condition,
                                                                           state)

        return is_applicable

    def _is_condition_applicable(self, preconditions: Precondition, state: State,
                                 problem_objects: Optional[Dict[str, PDDLObject]] = None) -> bool:
        """Validate if the given condition is applicable in the given state.

        :param preconditions: the condition to validate.
        :param state: the state to validate the condition in.
        :param problem_objects: the objects of the problem to use for universal preconditions.
        :return: whether the condition is applicable in the given state.
        """
        is_applicable = self._validate_equality_holds(preconditions)
        for condition in preconditions.operands:
            if isinstance(condition, GroundedPredicate):
                is_applicable = self._validate_predicates_hold(condition, is_applicable, preconditions, state)

            elif isinstance(condition, NumericalExpressionTree):
                is_applicable = self._validate_numeric_expression_hold(condition, is_applicable, preconditions, state)

            elif isinstance(condition, Precondition):
                is_applicable = BinaryOperator[preconditions.binary_operator](
                    is_applicable, self._is_condition_applicable(condition, state))

            elif isinstance(condition, UniversalPrecondition):
                is_applicable = self._validate_universal_precondition(condition, state, problem_objects)
                continue

            else:
                raise ValueError(f"Unknown precondition type: {type(condition)}")

        return is_applicable

    def ground_preconditions(self, parameters_map: Dict[str, str]) -> None:
        """Ground the preconditions of the action.

        :param parameters_map: the mapping between the lifted and the grounded objects.
        """
        self._grounded_precondition.root.equality_preconditions = \
            self._ground_equality_objects(self._lifted_precondition.root.equality_preconditions, parameters_map)
        self._grounded_precondition.root.inequality_preconditions = self._ground_equality_objects(
            self._lifted_precondition.root.inequality_preconditions, parameters_map)

        self._ground(lifted_conditions=self._lifted_precondition.root,
                     grounded_conditions=self._grounded_precondition.root, parameters_map=parameters_map)

    def is_applicable(self, state: State, problem_objects: Optional[Dict[str, PDDLObject]] = None) -> bool:
        """Check whether the precondition is satisfied in the given state.

        :param state: the state to check.
        :param problem_objects: the objects of the problem to use in universal preconditions.
        :return: True if the precondition is satisfied, False otherwise.
        """
        self.logger.debug(f"Validating if the preconditions hold in the state.")
        return self._is_condition_applicable(self._grounded_precondition.root, state, problem_objects)
