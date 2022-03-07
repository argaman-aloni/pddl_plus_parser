"""Module that represents a boolean predicate in a PDDL+ model."""
from typing import Dict, Optional

from .pddl_type import PDDLType

SignatureType = Dict[str, PDDLType]


class Predicate:
    """Class that represents a boolean predicate."""

    name: str
    signature: SignatureType

    def __init__(self, name: Optional[str] = None, signature: Optional[SignatureType] = None,
                 predicate: Optional["Predicate"] = None):
        if predicate:
            self.name = predicate.name
            self.signature = predicate.signature.copy()

        else:
            self.name = name
            self.signature = signature

    def __eq__(self, other: "Predicate") -> bool:
        """Checks whether or not two predicates are considered equal.

        Equality can be considered if a type inherits from another type as well.

        :param other: the other predicate to compare.
        :return: whether or not the predicates are equal.
        """
        if not self.name == other.name:
            return False

        for parameter_name, parameter_type in self.signature.items():
            if parameter_name not in other.signature:
                return False

            other_param_type = other.signature[parameter_name]
            if not parameter_type.is_sub_type(other_param_type):
                return False

        return True

    @property
    def untyped_representation(self) -> str:
        untyped_signature_str = " ".join(self.signature.keys())
        return f"({self.name} {untyped_signature_str})"

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    def __hash__(self):
        return hash(self.__str__())


class GroundedPredicate(Predicate):
    """Class defining a grounded predicate."""
    object_mapping: Dict[str, str]

    def __init__(self, name: str, signature: SignatureType, object_mapping: Dict[str, str]):
        super(GroundedPredicate, self).__init__(name=name, signature=signature)
        self.object_mapping = object_mapping

    def __eq__(self, other: "GroundedPredicate") -> bool:
        """Checks whether or not two grounded predicates are considered equal.

        Equality can be considered if a type inherits from another type as well.

        :param other: the other predicate to compare.
        :return: whether or not the predicates are equal.
        """
        if not super(GroundedPredicate, self).__eq__(other):
            return False

        return self.object_mapping == other.object_mapping

    @property
    def untyped_representation(self) -> str:
        untyped_grounded_signature_str = " ".join(self.object_mapping.values())
        return f"({self.name} {untyped_grounded_signature_str})"

    @property
    def lifted_typed_representation(self) -> str:
        return super().__str__()

    @property
    def lifted_untyped_representation(self) -> str:
        return super().untyped_representation

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{self.object_mapping[parameter_name]} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    def __hash__(self):
        return hash(self.__str__())
