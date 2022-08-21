"""This module exports the domain object to a domain file."""
from collections import defaultdict
from pathlib import Path
from typing import NoReturn, List, Dict, Set

from pddl_plus_parser.models import Predicate, Action, Domain, PDDLConstant, PDDLFunction, PDDLType


class DomainExporter:
    """Class that is able to export a domain to a correct PDDL file."""

    @staticmethod
    def write_action_predicates(positive_predicates: Set[Predicate], negative_predicates: Set[Predicate]) -> str:
        """Write the effects of an action according to the PDDL file format.

        :param positive_predicates: the add effects of an action.
        :param negative_predicates: the delete effects of an action.
        :return: the formatted string representing the action's predicates (preconditions or effects).
        """
        action_effect_predicates = [predicate.untyped_representation for predicate in positive_predicates]
        action_effect_predicates.extend(
            [f"(not {predicate.untyped_representation})" for predicate in negative_predicates])
        formatted_effects = "{content}"
        return formatted_effects.format(content=" ".join(action_effect_predicates))

    def write_action(self, action: Action) -> str:
        """Write the action formatted string from the action data.

        :param action: The action that needs to be formatted into a string.
        :return: the string format of the action.
        """
        action_params = " ".join(
            [f"{name} - {parameter_type.name}" for name, parameter_type in action.signature.items()])

        discrete_preconditions = self.write_action_predicates(action.positive_preconditions,
                                                              action.negative_preconditions)
        discrete_preconditions = f"(and {discrete_preconditions})"
        numeric_preconditions = "\n\t\t".join([fluent.to_pddl() for fluent in action.numeric_preconditions])
        if len(numeric_preconditions) > 0:
            numeric_preconditions += "\n"

        discrete_effects = self.write_action_predicates(action.add_effects, action.delete_effects)
        numeric_effects = "\n\t".join([fluent.to_pddl() for fluent in action.numeric_effects])
        if len(numeric_effects) > 0:
            numeric_effects += "\n"

        return f"(:action {action.name}\n" \
               f"\t:parameters   ({action_params})\n" \
               f"\t:precondition {discrete_preconditions}\n{numeric_preconditions}" \
               f"\t:effect       (and {discrete_effects}\n{numeric_effects})" \
               f")\n"

    @staticmethod
    def write_predicates(predicates: Dict[str, Predicate]) -> str:
        """Writes the predicates formatted according to the domain file format.

        :param predicates: the predicates that are in the domain's definition.
        :return: the formatted string representing the domain's predicates.
        """
        predicates_str = "(:predicates\n{predicates})\n\n"
        predicates_strings = []
        for predicate_name, predicate in predicates.items():
            predicate_params = " ".join(
                [f"{name} - {types[0]}" for name, types in predicate.signature])
            predicates_strings.append(f"\t({predicate_name} {predicate_params})")

        return predicates_str.format(predicates="\n".join(predicates_strings))

    @staticmethod
    def write_constants(constants: Dict[str, PDDLConstant]) -> str:
        """Writes the constants of the domain to the new domain file.

        :param constants: the constants that appear in the domain object.
        :return: the representation of the constants as a canonical PDDL string.
        """
        same_type_constant = defaultdict(list)
        for const_name, constant in constants.items():
            if const_name == "object":
                continue

            same_type_constant[constant.type.name].append(const_name)

        types_strs = []
        for constant_type_name, constant_objects in same_type_constant.items():
            types_strs.append(f"\t{' '.join(constant_objects)} - {constant_type_name}")

        return "\n".join(types_strs)

    @staticmethod
    def format_type_like_string(sorted_type_like_objects: Dict[str, List[str]]) -> List[str]:
        """formats the string that are of the same format as types. This applies to both consts and types.

        :param sorted_type_like_objects: the type like objects that are being formatted into a list of strings.
        :return: the formatted strings as a list.
        """
        type_like_object_content = []
        for pddl_type_name, sub_types in sorted_type_like_objects.items():
            type_like_object_pddl_str = "\t"
            type_like_object_pddl_str += "\n\t".join([child_type for child_type in sub_types[:-1]])
            type_like_object_pddl_str += f"\n\t{sub_types[-1]} - {pddl_type_name}"
            type_like_object_content.append(type_like_object_pddl_str)

        return type_like_object_content

    @staticmethod
    def write_types(types: Dict[str, PDDLType]) -> str:
        """Writes the definitions of the types according to the PDDL file format.

        :param types: the types that are available in the learned domain.
        :return: the formatted string representing the types in the PDDL domain file.
        """
        parent_child_map = defaultdict(list)
        for type_name, type_obj in types.items():
            if type_name == "object":
                continue

            parent_child_map[type_obj.parent.name].append(type_name)

        types_strs = []
        for parent_type, children_types in parent_child_map.items():
            types_strs.append(f"\t{' '.join(children_types)} - {parent_type}")

        return "\n".join(types_strs)

    @staticmethod
    def write_functions(functions: Dict[str, PDDLFunction]) -> str:
        """Converts the functions to PDDL format.

        :return: the PDDL format of the functions.
        """
        return "\n\t".join([str(f) for f in functions.values()])

    def extract_domain(self, domain: Domain) -> str:
        """Export the domain object to a correct PDDL file.

        :param domain: the learned domain object.
        """
        predicates = "\n\t".join([str(p) for p in domain.predicates.values()])
        actions = "\n".join(self.write_action(action) for action in domain.actions.values())
        constants = f"(:constants {self.write_constants(domain.constants)}\n)\n\n" if len(domain.constants) > 0 else ""
        functions = f"(:functions {self.write_functions(domain.functions)}\n)\n\n" if len(domain.functions) > 0 else ""
        return f"(define (domain {domain.name})\n" \
               f"(:requirements {' '.join(domain.requirements)})\n" \
               f"(:types {self.write_types(domain.types)}\n)\n\n" \
               f"(:predicates {predicates}\n)\n\n" \
               f"{constants}" \
               f"{functions}" \
               f"{actions}\n)"

    def export_domain(self, domain: Domain, export_path: Path) -> NoReturn:
        """Export the domain object to a correct PDDL file.

        :param domain: the domain object to be exported.
        :param export_path: the path to export the domain to.
        """
        domain_str = self.extract_domain(domain)
        with open(export_path, "wt") as export_domain_file:
            export_domain_file.write(domain_str)
