"""Module that represents a PDDL+ action."""

from typing import Set, List, Dict

from .conditional_effect import ConditionalEffect, UniversalEffect
from .numerical_expression import NumericalExpressionTree, DEFAULT_DIGITS
from .pddl_precondition import CompoundPrecondition
from .pddl_predicate import SignatureType, Predicate


class Action:
    """Class representing an instantaneous action in a PDDL+ problems."""

    name: str
    signature: SignatureType
    preconditions: CompoundPrecondition

    discrete_effects: Set[Predicate]
    conditional_effects: Set[ConditionalEffect]
    universal_effects: Set[UniversalEffect]
    numeric_effects: Set[NumericalExpressionTree]

    def __init__(self, name: str = None, signature: SignatureType = None):
        self.name = name if name is not None else ""
        self.signature = signature if signature is not None else {}
        self.discrete_effects = set()
        self.numeric_effects = set()
        self.conditional_effects = set()
        self.universal_effects = set()
        self.preconditions = CompoundPrecondition()  # type: ignore

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    @property
    def parameter_names(self) -> List[str]:
        return list(self.signature.keys())

    def signature_to_pddl(self) -> str:
        """Converts the action's signature to the PDDL format.

        :return: the PDDL format of the signature.
        """
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({signature_str})"

    def effects_to_pddl(self) -> str:
        """Converts the effects to the needed PDDL format.

        :return: the PDDL format of the effects.
        """
        simple_effects = "\n\t\t".join(sorted([effect.untyped_representation for effect in self.discrete_effects]))

        conditional_effects = "\n\t\t"
        conditional_effects += "\t\t\n".join(
            [str(conditional_effect) for conditional_effect in self.conditional_effects]
        )

        universal_effects = "\n\t\t"
        universal_effects += "\t\t\n".join([str(universal_effect) for universal_effect in self.universal_effects])

        if len(self.numeric_effects) > 0:
            numeric_effects = "\t\t\n".join([effect.to_pddl() for effect in self.numeric_effects])
            return (
                f"(and {simple_effects}\n"
                f"\t\t{conditional_effects}\n"
                f"\t\t{universal_effects}\n"
                f"{numeric_effects})"
            )

        return f"(and {simple_effects} {conditional_effects} {universal_effects})"

    def change_signature(self, old_to_new_parameter_names: Dict[str, str]) -> None:
        """Changes the action's signature.

        old_to_new_parameter_names: the mapping between the old and new parameter names.
        """
        ordered_old_signature = list(self.signature.keys())
        for old_param_name in ordered_old_signature:
            new_param_name = old_to_new_parameter_names[old_param_name]
            self.signature[new_param_name] = self.signature.pop(old_param_name)

        self.preconditions.change_signature(old_to_new_parameter_names)
        for effect in self.discrete_effects:
            effect.change_signature(old_to_new_parameter_names)

        for effect in self.numeric_effects:
            effect.change_signature(old_to_new_parameter_names)

        # TODO: change the signature of the conditional and universal effects.

    def to_pddl(self, decimal_digits: int = DEFAULT_DIGITS) -> str:
        """Returns the PDDL string representation of the action.

        :param decimal_digits: the number of decimal digits to use to display the preconditions.
        :return: the PDDL string representing the action.
        """
        action_string = (
            f"(:action {self.name}\n"
            f"\t:parameters {self.signature_to_pddl()}\n"
            f"\t:precondition {self.preconditions.print(decimal_digits=decimal_digits)}\n"
            f"\t:effect {self.effects_to_pddl()})"
        )
        formatted_string = "\n".join([line for line in action_string.split("\n") if line.strip()])
        return f"{formatted_string}\n"

        # for effect in self.conditional_effects:
