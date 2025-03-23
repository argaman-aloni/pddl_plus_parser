"""Module that represents a PDDL+ action."""
from typing import Set, List, Dict

from .conditional_effect import ConditionalEffect, UniversalEffect
from .numerical_expression import NumericalExpressionTree
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

    def __init__(self):
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

    def effects_to_pddl(self) -> str:
        """Converts the effects to the needed PDDL format.

        :return: the PDDL format of the effects.
        """
        simple_effects = "\n\t\t".join(
            sorted([effect.untyped_representation for effect in self.discrete_effects])
        )

        conditional_effects = "\n\t\t"
        conditional_effects += "\t\t\n".join(
            [str(conditional_effect) for conditional_effect in self.conditional_effects]
        )

        universal_effects = "\n\t\t"
        universal_effects += "\t\t\n".join(
            [str(universal_effect) for universal_effect in self.universal_effects]
        )

        if len(self.numeric_effects) > 0:
            numeric_effects = "\t\t\n".join(
                [effect.to_pddl() for effect in self.numeric_effects]
            )
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
        for old_param_name, new_param_name in old_to_new_parameter_names.items():
            self.signature[new_param_name] = self.signature.pop(old_param_name)

        self.preconditions.change_signature(old_to_new_parameter_names)
        for effect in self.discrete_effects:
            effect.change_signature(old_to_new_parameter_names)

        for effect in self.numeric_effects:
            effect.change_signature(old_to_new_parameter_names)

        # TODO: change the signature of the conditional and universal effects.
