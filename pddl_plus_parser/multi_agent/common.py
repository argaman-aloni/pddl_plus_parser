from typing import List

from pddl_plus_parser.models import Problem, State, ActionCall, Domain, Operator


def create_initial_state(problem: Problem) -> State:
    """Create the initial state of the problem.

    :param problem: the problem object.
    :return: the initial state of the problem.
    """
    initial_state_predicates = problem.initial_state_predicates
    initial_state_numeric_fluents = problem.initial_state_fluents
    return State(predicates=initial_state_predicates, fluents=initial_state_numeric_fluents, is_init=True)


def apply_actions(domain: Domain, current_state: State, joint_action: List[ActionCall]) -> State:
    """

    :param domain: the domain with the action scheme.
    :param current_state: the current state that the action is being applied on.
    :param joint_action: the executable actions of the agents.
    :return:
    """
    interm_state_predicates = current_state.state_predicates.copy()
    interm_state_numeric_fluents = current_state.state_fluents.copy()
    operators = []
    for action_call in joint_action:
        action = domain.actions[action_call.name]
        operator = Operator(action=action, domain=domain, grounded_action_call=action_call.parameters)
        partial_numeric_state = State(predicates=interm_state_predicates, fluents=interm_state_numeric_fluents)
        partial_next_state = operator.apply(partial_numeric_state)
        interm_state_predicates.update(partial_next_state.state_predicates)
        interm_state_numeric_fluents.update(partial_next_state.state_fluents)
        operators.append(operator)

    return State(predicates=interm_state_predicates, fluents=interm_state_numeric_fluents)
