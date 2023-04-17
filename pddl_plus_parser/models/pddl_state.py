"""Module that represents a state definition in a PDDL trajectory."""
from typing import Dict, Set

from .pddl_function import PDDLFunction
from .pddl_predicate import GroundedPredicate


class State:
    """A representation of a state in a trajectory."""

    is_init: bool
    # Maps between a lifted predicate definition to all of its problem groundings
    state_predicates: Dict[str, Set[GroundedPredicate]]
    # Map between the grounded numeric fluent string to the actual function.
    state_fluents: Dict[str, PDDLFunction]

    def __init__(self, predicates: Dict[str, Set[GroundedPredicate]],
                 fluents: Dict[str, PDDLFunction], is_init: bool = False):
        self.state_predicates = predicates
        self.state_fluents = fluents
        self.is_init = is_init

    def _serialize_numeric_fluents(self) -> str:
        """Serialize the numeric fluents of the state.

        :return: the string representing the assigned grounded fluents.
        """
        return " ".join(fluent.state_representation for fluent in self.state_fluents.values())

    def _serialize_predicates(self) -> str:
        """Serialize the predicates the constitute the state's facts.

        :return: the string representation of the state's facts. 
        """
        predicates_str = ""
        for grounded_predicates in self.state_predicates.values():
            predicates_str += " "
            predicates_str += " ".join(predicate.untyped_representation for predicate in grounded_predicates)

        return predicates_str

    def typed_serialize(self) -> str:
        """Returns a typed version of the serialized state.

        :return: typed version of the serialized state.
        """
        typed_predicates_str = ""
        for grounded_predicates in self.state_predicates.values():
            typed_predicates_str += " "
            typed_predicates_str += " ".join(str(predicate) for predicate in grounded_predicates)

        return f"({' '.join(fluent.state_typed_representation for fluent in self.state_fluents.values())}" \
               f"{typed_predicates_str})\n"

    def serialize(self) -> str:
        return f"({':init' if self.is_init else ':state'}" \
               f" {self._serialize_numeric_fluents()}" \
               f"{self._serialize_predicates()})\n"

    def copy(self) -> "State":
        """Creates a copy of the state."""
        copied_predicates = {predicate_name: {predicate.copy() for predicate in predicates} for
                             predicate_name, predicates
                             in self.state_predicates.items()}
        copied_fluents = {fluent_name: fluent.copy() for fluent_name, fluent in self.state_fluents.items()}
        return State(copied_predicates, copied_fluents, is_init=self.is_init)
