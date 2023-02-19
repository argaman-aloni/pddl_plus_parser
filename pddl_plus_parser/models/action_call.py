"""Module to contain all different types of action calls."""
from typing import List

NOP_ACTION = "nop"


class ActionCall:
    """An object representing a single action call."""
    name: str
    parameters: List[str]

    def __init__(self, name: str, grounded_parameters: List[str]):
        self.name = name
        self.parameters = grounded_parameters

    def __str__(self):
        called_objects = " ".join(self.parameters)
        return f"({self.name} {called_objects})"


class JointActionCall:
    """An object representing a single action call."""

    actions: List[ActionCall]

    def __init__(self, actions: List[ActionCall]):
        self.actions = actions

    def __str__(self) -> str:
        return f"[{','.join([str(action) for action in self.actions])}]"

    @property
    def action_count(self) -> int:
        return len([action for action in self.actions if action.name != NOP_ACTION])

    @property
    def operational_actions(self) -> List[ActionCall]:
        return [action for action in self.actions if action.name != NOP_ACTION]

    @property
    def joint_parameters(self) -> List[str]:
        params = []
        for action in self.actions:
            params.extend(action.parameters)

        return params
