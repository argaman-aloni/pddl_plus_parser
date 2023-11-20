"""Module that encapsulates the functionality of grounded effects."""
import logging
from typing import Set, Dict, Optional

from pddl_plus_parser.models.grounded_precondition import GroundedPrecondition
from pddl_plus_parser.models.grounding_utils import ground_predicate, ground_numeric_calculation_tree
from pddl_plus_parser.models.numerical_expression import NumericalExpressionTree, evaluate_expression, \
    set_expression_value
from pddl_plus_parser.models.pddl_action import Action
from pddl_plus_parser.models.pddl_domain import Domain
from pddl_plus_parser.models.pddl_function import PDDLFunction
from pddl_plus_parser.models.pddl_precondition import CompoundPrecondition
from pddl_plus_parser.models.pddl_predicate import Predicate, GroundedPredicate
from pddl_plus_parser.models.pddl_state import State


class GroundedEffect:
    """Class that represents the grounded version of an action's effect."""
    _lifted_discrete_effects: Set[Predicate]
    _lifted_numeric_effects: Set[NumericalExpressionTree]

    grounded_antecedents: GroundedPrecondition
    grounded_discrete_effects: Set[GroundedPredicate]
    grounded_numeric_effects: Set[NumericalExpressionTree]

    def __init__(self, lifted_antecedents: Optional[CompoundPrecondition],
                 lifted_discrete_effects: Set[Predicate], lifted_numeric_effects: Set[NumericalExpressionTree],
                 domain: Domain, action: Action):
        self.grounded_antecedents = GroundedPrecondition(lifted_antecedents, domain,
                                                         action) if lifted_antecedents is not None else None
        self._lifted_discrete_effects = lifted_discrete_effects
        self._lifted_numeric_effects = lifted_numeric_effects
        self.domain = domain
        self.action = action
        self.grounded_discrete_effects = set()
        self.grounded_numeric_effects = set()
        self.logger = logging.getLogger(__name__)

    def ground_conditional_effect(self, parameters_map: Dict[str, str]) -> None:
        """Grounds the conditional effect.

        :param parameters_map: the mapping between the lifted action's parameters and the objects using which the action
            is applied with.
        """
        if self.grounded_antecedents is not None:
            self.grounded_antecedents.ground_preconditions(parameters_map)

        for effect in self._lifted_discrete_effects:
            self.grounded_discrete_effects.add(ground_predicate(effect, parameters_map, self.domain, self.action))

        for effect in self._lifted_numeric_effects:
            self.grounded_numeric_effects.add(ground_numeric_calculation_tree(effect, parameters_map, self.domain))

    def antecedents_hold(self, state: State, allow_inapplicable_actions: bool = False) -> bool:
        """Checks whether the antecedents of the effect hold in the given state.

        :param state: the state that the effect is applied to.
        :param allow_inapplicable_actions: whether to allow inapplicable actions.
        :return: whether the antecedents hold in the given state.
        """
        if self.grounded_antecedents is None or allow_inapplicable_actions:
            return True

        return self.grounded_antecedents.is_applicable(state)

    def _apply_discrete_effects(self, next_state_predicates: Dict[str, Set[GroundedPredicate]]) -> None:
        """Applies the discrete effects to the given state.

        Note: This method works according to the delete then add semantics of PDDL+.

        :param next_state_predicates: the next state predicates to update with the effect's data.
        """
        # delete effects
        delete_effects = [effect for effect in self.grounded_discrete_effects if not effect.is_positive]
        add_effects = [effect for effect in self.grounded_discrete_effects if effect.is_positive]
        for predicate in delete_effects:
            positive_predicate = predicate.copy()
            positive_predicate.is_positive = True
            if positive_predicate.lifted_untyped_representation not in next_state_predicates:
                continue

            for state_predicate in next_state_predicates[positive_predicate.lifted_untyped_representation]:
                if state_predicate.untyped_representation == positive_predicate.untyped_representation:
                    next_state_predicates[positive_predicate.lifted_untyped_representation].discard(state_predicate)
                    break

        for predicate in add_effects:
            lifted_predicate_str = predicate.lifted_untyped_representation
            next_state_grounded_predicates = next_state_predicates.get(lifted_predicate_str, set())
            next_state_grounded_predicates.add(predicate)
            next_state_predicates[lifted_predicate_str] = next_state_grounded_predicates

    @staticmethod
    def _update_single_numeric_expression(numeric_expression: NumericalExpressionTree,
                                          values_to_update: Dict[str, PDDLFunction]) -> None:
        """Updates the numeric value of a single numeric expression.

        :param numeric_expression: the expression that represents the change to the state.
        :param values_to_update: the previous values of the numeric expressions in the state to be updated.
        """
        set_expression_value(numeric_expression.root, values_to_update)
        new_grounded_function = evaluate_expression(numeric_expression.root)
        values_to_update[new_grounded_function.untyped_representation] = new_grounded_function

    def apply(self, state: State) -> None:
        """Applies the effect to the given state.

        :param state: the state in which the effect is applied.
        """
        self.logger.debug("The antecedents for the effect hold so applying the effect.")
        self._apply_discrete_effects(next_state_predicates=state.state_predicates)
        for grounded_expression in self.grounded_numeric_effects:
            self._update_single_numeric_expression(grounded_expression, values_to_update=state.state_fluents)
