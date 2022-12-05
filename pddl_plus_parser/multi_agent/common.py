from collections import defaultdict
from typing import List

from pddl_plus_parser.models import Problem, State, ActionCall, Domain, Operator, GroundedPredicate, \
    NOP_ACTION


def create_initial_state(problem: Problem) -> State:
    """Create the initial state of the problem.

    :param problem: the problem object.
    :return: the initial state of the problem.
    """
    initial_state_predicates = problem.initial_state_predicates
    initial_state_numeric_fluents = problem.initial_state_fluents
    return State(predicates=initial_state_predicates, fluents=initial_state_numeric_fluents, is_init=True)


def apply_actions(domain: Domain, current_state: State, joint_action: List[ActionCall],
                  allow_inapplicable_actions: bool = False) -> State:
    """

    :param domain: the domain with the action scheme.
    :param current_state: the current state that the action is being applied on.
    :param joint_action: the executable actions of the agents.
    :param allow_inapplicable_actions: whether to allow inapplicable actions.
    :return: The state resulting from applying the actions.
    """
    operators = []
    if len(joint_action) == 1:
        action_call = joint_action[0]
        action = domain.actions[action_call.name]
        return Operator(action=action, domain=domain, grounded_action_call=action_call.parameters).apply(
            previous_state=current_state, allow_inapplicable_actions=allow_inapplicable_actions)

    accumulative_discrete_effects = defaultdict(set)
    accumulative_numeric_effects = current_state.state_fluents.copy()
    for lifted_name, grounded_predicates in current_state.state_predicates.items():
        for predicate in grounded_predicates:
            accumulative_discrete_effects[lifted_name].add(GroundedPredicate(predicate.name, predicate.signature,
                                                                             predicate.object_mapping))

    for action_call in joint_action:
        if action_call.name == NOP_ACTION:
            continue

        action = domain.actions[action_call.name]
        operator = Operator(action=action, domain=domain, grounded_action_call=action_call.parameters)
        partial_numeric_state = State(predicates=current_state.state_predicates, fluents=accumulative_numeric_effects)
        partial_next_state = operator.apply(partial_numeric_state)
        accumulative_numeric_effects.update(partial_next_state.state_fluents)
        # since there are multiple actions being executed at once, we need to take the difference between the
        # current state and the next state and accumulate it.
        for delete_effect in operator.grounded_delete_effects:
            for grounded_predicate in accumulative_discrete_effects[delete_effect.lifted_untyped_representation]:
                if grounded_predicate.untyped_representation == delete_effect.untyped_representation:
                    accumulative_discrete_effects[delete_effect.lifted_untyped_representation].remove(
                        grounded_predicate)
                    break

        for add_effect in operator.grounded_add_effects:
            accumulative_discrete_effects[add_effect.lifted_untyped_representation].add(add_effect)

        operators.append(operator)

    return State(predicates=accumulative_discrete_effects, fluents=accumulative_numeric_effects)
