"""Module that represents a numerical in a PDDL+ model."""
from typing import Optional, NoReturn

from .pddl_predicate import SignatureType


class PDDLFunction:
    """Class that represents a numerical function."""

    name: str
    signature: SignatureType
    stored_value: float

    def __init__(self, name: Optional[str] = None, signature: Optional[SignatureType] = None):
        self.name = name
        self.signature = signature
        self.stored_value = 0

    def __eq__(self, other: "PDDLFunction") -> bool:
        """Checks whether two functions are considered equal.

        Equality can be considered if a type inherits from another type as well.

        :param other: the other predicate to compare.
        :return: whether the predicates are equal.
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
    def value(self) -> float:
        return self.stored_value

    def set_value(self, value: float) -> NoReturn:
        """Set the value of a function to be the input value.

        :param value: the value to set to the function.
        """
        self.stored_value = value

    @property
    def state_representation(self) -> str:
        untyped_signature_str = " ".join(self.signature.keys())
        return f"(= ({self.name} {untyped_signature_str}) {self.value})"

    @property
    def state_typed_representation(self) -> str:
        signature_str_items = [f"{parameter_name} - {str(parameter_type)}"
                               for parameter_name, parameter_type in self.signature.items()]
        return f"(= ({self.name} {' '.join(signature_str_items)}) {self.value})"

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
