"""Module that represents a numerical in a PDDL+ model."""
from typing import Optional, Dict

from .pddl_predicate import SignatureType


class PDDLFunction:
    """Class that represents a numerical function."""

    name: str
    signature: SignatureType
    stored_value: float
    repeating_variables: Dict[str, int]

    def __init__(
        self,
        name: Optional[str] = None,
        signature: Optional[SignatureType] = None,
        repeating_variables: Optional[Dict[str, int]] = {},
    ):
        self.name = name
        self.signature = signature
        self.stored_value = 0
        self.repeating_variables = repeating_variables

    def __eq__(self, other: "PDDLFunction") -> bool:
        """Checks whether two functions are considered equal.

        Equality can be considered if a type inherits from another type as well.

        :param other: the other predicate to compare.
        :return: whether the predicates are equal.
        """
        if not isinstance(other, PDDLFunction) or other is None:
            return False

        if not self.name == other.name:
            return False

        # check that the parameters are the same (including their order) -- assuming dict keys are ordered
        if list(self.signature.keys()) != list(other.signature.keys()):
            return False

        for parameter_name, parameter_type in self.signature.items():
            if parameter_name not in other.signature:
                return False

            other_param_type = other.signature[parameter_name]
            if not parameter_type.is_sub_type(other_param_type):
                return False

        if self.stored_value != other.stored_value:
            return False

        return True

    def copy(self) -> "PDDLFunction":
        """Creates a copy of the function."""
        copied_function = PDDLFunction(
            self.name, self.signature, self.repeating_variables
        )
        copied_function.stored_value = self.stored_value
        return copied_function

    @property
    def value(self) -> float:
        return self.stored_value

    def set_value(self, value: float) -> None:
        """Set the value of a function to be the input value.

        :param value: the value to set to the function.
        """
        self.stored_value = value

    @property
    def state_representation(self) -> str:
        """Returns the state representation of the function."""
        function_variables = []
        for repeating_variable, num_repeats in self.repeating_variables.items():
            function_variables.extend([repeating_variable] * num_repeats)
        function_variables.extend(
            param for param in self.signature if param not in self.repeating_variables
        )

        untyped_signature_str = " ".join(function_variables)
        return f"(= ({self.name} {untyped_signature_str}) {self.value})"

    @property
    def state_typed_representation(self) -> str:
        """Returns the state representation of the function with the type signature."""
        function_variables = []
        for repeating_variable, num_repeats in self.repeating_variables.items():
            function_variables.extend([repeating_variable] * num_repeats)
        function_variables.extend(
            param for param in self.signature if param not in self.repeating_variables
        )

        signature_str_items = [
            f"{parameter_name} - {str(self.signature[parameter_name])}"
            for parameter_name in function_variables
        ]
        return f"(= ({self.name} {' '.join(signature_str_items)}) {self.value})"

    @property
    def untyped_representation(self) -> str:
        """Returns the representation of the function without the type information.

        Note:
            This property is used only for lifted assignments so no need to check for the grounded items' multiplicity.
        """
        untyped_signature_str = " ".join(self.signature.keys())
        return f"({self.name} {untyped_signature_str})"

    def change_signature(self, old_to_new_param_names: Dict[str, str]) -> None:
        """Performs inline changing of the function's signature.

        :param old_to_new_param_names: the mapping of old parameter names to new parameter names.
        """
        ordered_old_parameters = list(self.signature.keys())
        for old_param_name in ordered_old_parameters:
            new_param_name = old_to_new_param_names[old_param_name]
            self.signature[new_param_name] = self.signature.pop(old_param_name)

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"
