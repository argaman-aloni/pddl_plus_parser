"""Module to represent an observed trajectory. Compared to a trajectory, this contains only the observed data."""
from typing import List, Dict

from pddl_plus_parser.models.action_call import ActionCall, JointActionCall
from pddl_plus_parser.models.pddl_object import PDDLObject
from pddl_plus_parser.models.pddl_state import State


class ObservedComponent:
    """Class representing a single observed component."""

    previous_state: State
    grounded_action_call: ActionCall
    next_state: State
    is_successful: bool

    def __init__(
        self,
        previous_state: State,
        call: ActionCall,
        next_state: State,
        is_successful: bool = True,
    ):
        self.previous_state = previous_state
        self.grounded_action_call = call
        self.next_state = next_state
        self.is_successful = is_successful

    def __str__(self):
        return (
            f"previous state: {self.previous_state.serialize()}\n"
            f"operator: {str(self.grounded_action_call)}\n"
            f"next state: {self.next_state.serialize()}"
        )

    def copy(self) -> "ObservedComponent":
        """Creates a deep copy of the observed component."""
        return ObservedComponent(
            previous_state=self.previous_state.copy(),
            call=self.grounded_action_call.copy(),
            next_state=self.next_state.copy(),
            is_successful=self.is_successful
        )


class MultiAgentComponent:
    """class representing a multi-agent observed component."""

    previous_state: State
    grounded_joint_action: JointActionCall
    next_state: State
    is_successful: bool

    def __init__(
        self,
        previous_state: State,
        joint_action: List[ActionCall],
        next_state: State,
        is_successful: bool = True,
    ):
        self.previous_state = previous_state
        self.grounded_joint_action = JointActionCall(joint_action)
        self.next_state = next_state
        self.is_successful = is_successful

    def __str__(self):
        return (
            f"previous state: {self.previous_state.serialize()}\n"
            f"operators: {str(self.grounded_joint_action)}\n"
            f"next state: {self.next_state.serialize()}"
        )


class Observation:
    """Class representing an observed trajectory data."""

    components: List[ObservedComponent]
    grounded_objects: Dict[str, PDDLObject]

    def __init__(self):
        self.components = []
        self.grounded_objects = {}

    def __len__(self):
        return len(self.components)

    def add_problem_objects(self, objects: Dict[str, PDDLObject]) -> None:
        """Add the objects from the problem to the observation data.

        :param objects: the objects from the problem.
        """
        self.grounded_objects = objects

    def add_component(
        self,
        previous_state: State,
        call: ActionCall,
        next_state: State,
        is_successful_transition: bool = True,
    ) -> None:
        """Add a new component to the observation data.

        :param previous_state: the state observed before the action call.
        :param call: the grounded action call.
        :param next_state: the state after the action was executed.
        :param is_successful_transition: whether the transition was successful.
        """
        self.components.append(
            ObservedComponent(
                previous_state, call, next_state, is_successful=is_successful_transition
            )
        )

    def copy(self) -> "Observation":
        """Creates a deep copy of the observation."""
        copied_observation = Observation()
        for component in self.components:
            copied_component = component.copy()
            copied_observation.components.append(copied_component)
        copied_observation.grounded_objects = {
            obj_name: obj.copy() for obj_name, obj in self.grounded_objects.items()
        }
        return copied_observation


class MultiAgentObservation:
    """Class representing an observed multi-agent trajectory data."""

    components: List[MultiAgentComponent]
    grounded_objects: Dict[str, PDDLObject]
    agents_in_observation: List[str]

    def __init__(self, executing_agents: List[str]):
        self.components = []
        self.grounded_objects = {}
        self.agents_in_observation = executing_agents

    def __len__(self):
        return len(self.components)

    def add_problem_objects(self, objects: Dict[str, PDDLObject]) -> None:
        """Add the objects from the problem to the observation data.

        :param objects: the objects from the problem.
        """
        self.grounded_objects = objects

    def add_component(
        self,
        previous_state: State,
        joint_action: List[ActionCall],
        next_state: State,
        is_successful_transition: bool = True,
    ) -> None:
        """Add a new component to the observation data.

        :param previous_state: the state observed before the action call.
        :param joint_action: the grounded joint action.
        :param next_state: the state after the action was executed.
        :param is_successful_transition: whether the transition was successful.
        """
        self.components.append(
            MultiAgentComponent(
                previous_state,
                joint_action,
                next_state,
                is_successful=is_successful_transition,
            )
        )
