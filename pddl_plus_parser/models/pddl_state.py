"""Module that represents a state definition in a PDDL trajectory."""
from typing import Dict, Set

from anytree import AnyNode

from . import NumericalExpressionTree
from .pddl_function import PDDLFunction
from .pddl_object import PDDLObject
from .pddl_predicate import GroundedPredicate


class State:
    """A representation of a state in a trajectory."""

    is_init: bool
    # Maps between a lifted predicate definition to all of its problem groundings
    state_predicates: Dict[str, Set[GroundedPredicate]]
    # Map between the grounded numeric fluent string to the actual function.
    state_fluents: Dict[str, PDDLFunction]

    def __init__(
        self,
        predicates: Dict[str, Set[GroundedPredicate]],
        fluents: Dict[str, PDDLFunction],
        is_init: bool = False,
    ):
        self.state_predicates = predicates
        self.state_fluents = fluents
        self.is_init = is_init

    def __eq__(self, other: "State") -> bool:
        my_predicates = {
            predicate.untyped_representation
            for ground_predicates in self.state_predicates.values()
            for predicate in ground_predicates
        }
        other_predicates = {
            predicate.untyped_representation
            for ground_predicates in other.state_predicates.values()
            for predicate in ground_predicates
        }
        if my_predicates != other_predicates:
            return False

        my_numeric_expressions = {
            expression.state_representation
            for expression in self.state_fluents.values()
        }
        other_numeric_expressions = {
            expression.state_representation
            for expression in other.state_fluents.values()
        }

        return my_numeric_expressions == other_numeric_expressions

    def _serialize_numeric_fluents(self) -> str:
        """Serialize the numeric fluents of the state.

        :return: the string representing the assigned grounded fluents.
        """
        return " ".join(
            fluent.state_representation for fluent in self.state_fluents.values()
        )

    def _serialize_predicates(self) -> str:
        """Serialize the predicates the constitute the state's facts.

        :return: the string representation of the state's facts.
        """
        predicates_str = ""
        for grounded_predicates in self.state_predicates.values():
            predicates_str += " "
            predicates_str += " ".join(
                predicate.untyped_representation for predicate in grounded_predicates
            )

        return predicates_str

    def typed_serialize(self) -> str:
        """Returns a typed version of the serialized state.

        :return: typed version of the serialized state.
        """
        typed_predicates_str = ""
        for grounded_predicates in self.state_predicates.values():
            typed_predicates_str += " "
            typed_predicates_str += " ".join(
                str(predicate) for predicate in grounded_predicates
            )

        return (
            f"({' '.join(fluent.state_typed_representation for fluent in self.state_fluents.values())}"
            f"{typed_predicates_str})\n"
        )

    def get_state_objects(self) -> Dict[str, PDDLObject]:
        """Returns all the objects in the state."""
        state_objects = {}
        for grounded_predicates_set in self.state_predicates.values():
            for grounded_predicate in grounded_predicates_set:
                for param_name, obj_type in grounded_predicate.signature.items():
                    object_name = grounded_predicate.object_mapping[param_name]
                    state_objects[object_name] = PDDLObject(
                        name=object_name, type=obj_type
                    )

        for grounded_function in self.state_fluents.values():
            for obj_name, obj_type in grounded_function.signature.items():
                state_objects[obj_name] = PDDLObject(name=obj_name, type=obj_type)

        return state_objects

    def serialize(self) -> str:
        return (
            f"({':init' if self.is_init else ':state'}"
            f" {self._serialize_numeric_fluents()}"
            f"{self._serialize_predicates()})\n"
        )

    def convert_fluents_to_numeric_conditions(self) -> Set[NumericalExpressionTree]:
        """Converts the numeric fluents to numerical conditions.

        :return: the set of numerical conditions representing the numeric fluents.
        """
        conditions = set()
        for fluent in self.state_fluents.values():
            left_child = AnyNode(id=str(fluent), value=fluent)
            right_child = AnyNode(id=str(fluent.value), value=fluent.value)
            root_node = AnyNode(id="=", value="=", children=[left_child, right_child])
            conditions.add(NumericalExpressionTree(root_node))

        return conditions

    def copy(self) -> "State":
        """Creates a copy of the state."""
        copied_predicates = {
            predicate_name: {predicate.copy() for predicate in predicates}
            for predicate_name, predicates in self.state_predicates.items()
        }
        copied_fluents = {
            fluent_name: fluent.copy()
            for fluent_name, fluent in self.state_fluents.items()
        }
        return State(copied_predicates, copied_fluents, is_init=self.is_init)
