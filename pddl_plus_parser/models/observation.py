"""Module to represent an observed trajectory. Compared to a trajectory, this contains only the observed data."""
from typing import List, NoReturn

from pddl_plus_parser.models.pddl_state import State


class ActionCall:
    """An object representing a single action call."""
    name: str
    parameters: List[str]

    def __init__(self, name: str, grounded_parameters: List[str]):
        self.name = name
        self.parameters = grounded_parameters


class ObservedComponent:
    """Class representing a single observed component."""

    previous_state: State
    grounded_action_call: ActionCall
    next_state: State

    def __init__(self, previous_state: State, call: ActionCall, next_state: State):
        self.previous_state = previous_state
        self.grounded_action_call = call
        self.next_state = next_state

    def __str__(self):
        return f"previous state: {self.previous_state.serialize()}\n" \
               f"operator: {str(self.grounded_action_call)}\n" \
               f"next state: {self.next_state.serialize()}"

class Observation:
    """Class representing an observed trajectory data."""

    components: List[ObservedComponent]

    def __init__(self):
        self.components = []

    def add_component(self, previous_state: State, call: ActionCall, next_state: State) -> NoReturn:
        """Add a new component to the observation data.

        :param previous_state: the state observed before the action call.
        :param call: the grounded action call.
        :param next_state: the state after the action was executed.
        """
        self.components.append(ObservedComponent(previous_state, call, next_state))

