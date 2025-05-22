"""Module that contains the parser for PDDL+ domain files."""
import logging
from pathlib import Path
from typing import List, Dict, Union

from pddl_plus_parser.models import (
    Domain,
    PDDLType,
    Predicate,
    PDDLConstant,
    PDDLFunction,
    Action,
    CompoundPrecondition,
    ObjectType,
)
from .effects_parser import EffectsParser
from .parsing_utils import parse_signature
from .pddl_tokenizer import PDDLTokenizer
from .preconditions_parser import PreconditionsParser


class DomainParser:
    """Class that parses PDDL+ domain files."""

    tokenizer: PDDLTokenizer
    logger: logging.Logger
    partial_parsing: bool
    enable_disjunctions: bool
    preconditions_parser: PreconditionsParser
    effects_parser: EffectsParser

    def __init__(
        self,
        domain_path: Path,
        partial_parsing: bool = False,
        enable_disjunctions: bool = False,
    ):
        self.tokenizer = PDDLTokenizer(domain_path)
        self.preconditions_parser = PreconditionsParser(self.tokenizer)
        self.effects_parser = EffectsParser(self.tokenizer)
        self.logger = logging.getLogger(__name__)
        self.partial_parsing = partial_parsing
        self.enable_disjunctions = enable_disjunctions

    def parse_types(self, types: List[str]) -> Dict[str, PDDLType]:
        """Parse the types of the domain.

        :param types: the list containing the
        :return: a mapping between the type name and the appropriate PDDLType object.
        """
        self.logger.info("Starting to parse the types in the domain!")
        pddl_types = {}
        same_types_objects = []
        index = 0
        while index < len(types):
            if types[index] != "-":
                same_types_objects.append(types[index])
                index += 1
                continue

            pddl_type = types[index + 1]
            parent_type = pddl_types.get(
                pddl_type, PDDLType(name=pddl_type, parent=ObjectType)
            )
            pddl_types.update(
                {
                    descendant_typ_name: PDDLType(
                        name=descendant_typ_name, parent=parent_type
                    )
                    for descendant_typ_name in same_types_objects
                }
            )
            same_types_objects = []
            index += 2
            continue

        if len(same_types_objects) > 0:
            pddl_types.update(
                {
                    type_name: PDDLType(name=type_name, parent=ObjectType)
                    for type_name in same_types_objects
                }
            )

        pddl_types["object"] = ObjectType
        self.logger.debug(
            f"Extracted {len(pddl_types)} types while parsing the types AST."
        )
        return pddl_types

    def parse_constants(
        self, constants_ast: List[str], domain_types: Dict[str, PDDLType]
    ) -> Dict[str, PDDLConstant]:
        """Parses the constants that appear in the constants part of the domain AST.

        :param constants_ast: the constants that were parsed in the domain AST.
        :param domain_types: the types that exist in the domain.
        :return: a list containing all typed constants.
        """
        self.logger.info("Starting to parse the constants of the domain!")
        constants = {}
        same_type_constants = []
        type_marker_reached = False
        for constant_name in constants_ast:
            if type_marker_reached:
                # This means that the name of the constant here is actually its type.
                if constant_name not in domain_types:
                    raise SyntaxError("Received invalid type for the constants!")

                constants.update(
                    {
                        name: PDDLConstant(name, domain_types[constant_name])
                        for name in same_type_constants
                    }
                )
                type_marker_reached = False
                same_type_constants = []
                continue

            if constant_name == "-":
                type_marker_reached = True
                continue

            same_type_constants.append(constant_name)

        self.logger.debug(f"Extracted {len(constants)} from the domain.")
        return constants

    def _parse_predicate(
        self, predicate_ast: List[str], domain_types: Dict[str, PDDLType]
    ) -> Predicate:
        """Parse a single predicate from an AST representation in the PDDL domain.

        :param predicate_ast: the predicate in the form of an AST list of strings.
        :param domain_types: the types that were extracted from the domain.
        :return: the predicate object that represents the list of strings that were given.
        """
        self.logger.info(
            f"Parsing the predicate represented by the AST - {predicate_ast}"
        )
        predicate_name = predicate_ast[0]
        signature_items = iter(predicate_ast[1:])
        predicate_signature = parse_signature(signature_items, domain_types)
        extracted_predicate = Predicate(
            name=predicate_name, signature=predicate_signature, is_positive=True
        )
        self.logger.debug(f"Finished extracting the predicate - {extracted_predicate}")
        return extracted_predicate

    def parse_predicates(
        self, predicates_ast: List[List[str]], domain_types: Dict[str, PDDLType]
    ) -> Dict[str, Predicate]:
        """Parses the predicates that appear in the predicates parsed AST.

        :param predicates_ast: the AST that contains the predicates of the domain.
        :param domain_types: the types that exist in the domain.
        :return: a mapping between the predicate name and the predicate itself.
        """
        self.logger.debug(
            "Assuming that all the predicates defined in the domain are positive."
        )
        predicates = {}
        for predicate in predicates_ast:
            if predicate[0] == ":private":
                for private_predicate in predicate[1:]:
                    extracted_private_predicate = self._parse_predicate(
                        private_predicate, domain_types
                    )
                    predicates[
                        extracted_private_predicate.name
                    ] = extracted_private_predicate

                continue

            extracted_predicate = self._parse_predicate(predicate, domain_types)
            predicates[extracted_predicate.name] = extracted_predicate

        return predicates

    def parse_functions(
        self, functions_ast: List[List[str]], domain_types: Dict[str, PDDLType]
    ) -> Dict[str, PDDLFunction]:
        """Parses the functions that appear in the functions parsed AST.

        :param functions_ast: the AST that contains the numerical functions of the domain.
        :param domain_types: the types that exist in the domain.
        :return: a mapping between a function name and the function itself.
        """
        self.logger.info(
            "Starting to parse the function' definition in the domain data."
        )
        functions = {}
        for function_items in functions_ast:
            function_name = function_items[0]
            if (len(function_items[1:]) % 3) != 0:
                raise SyntaxError(
                    f"Received a function with a wrong signature - {function_items[1:]}"
                )

            signature_items = iter(function_items[1:])
            function_signature = parse_signature(signature_items, domain_types)
            functions[function_name] = PDDLFunction(
                name=function_name, signature=function_signature
            )

        return functions

    def parse_preconditions(
        self,
        preconditions_ast: List[Union[str, List[str]]],
        new_action: Action,
        domain_functions: Dict[str, PDDLFunction],
        domain_predicates: Dict[str, Predicate],
        domain_types: Dict[str, PDDLType],
        domain_constants: Dict[str, PDDLConstant],
    ) -> None:
        """Parse the preconditions of a single action.

        :param preconditions_ast: the AST representation of the action's preconditions.
        :param new_action: the action that is currently being parsed.
        :param domain_functions: the functions that exist in the domain.
        :param domain_predicates: the predicates that exist in the domain.
        :param domain_types: the types that exist in the domain.
        :param domain_constants: the constants that might exist in the domain.
        """
        if len(preconditions_ast) == 0:
            self.logger.warning("Received an action with no preconditions.")
            return

        if preconditions_ast[0] != "and" and len(preconditions_ast[1:]) > 1:
            raise SyntaxError(
                f"Only accepting conjunctive preconditions! Action - {new_action.name} does not conform!"
            )

        action_preconditions = CompoundPrecondition()
        self.preconditions_parser.parse(
            precondition_root=action_preconditions.root,
            preconditions_ast=preconditions_ast[1:],
            domain_functions=domain_functions,
            domain_types=domain_types,
            domain_predicates=domain_predicates,
            domain_constants=domain_constants,
            action_signature=new_action.signature,
        )
        new_action.preconditions = action_preconditions

    def parse_effects(
        self,
        effects_ast: List[Union[str, List[str]]],
        new_action: Action,
        domain_types: Dict[str, PDDLType],
        domain_functions: Dict[str, PDDLFunction],
        domain_predicates: Dict[str, Predicate],
        domain_constants: Dict[str, PDDLConstant],
    ) -> None:
        """Parse the effects of a single action.

        :param effects_ast: the AST representation of the action's effects.
        :param new_action: the action that is currently being parsed.
        :param domain_types: the types that exist in the domain.
        :param domain_functions: the functions that exist in the domain.
        :param domain_predicates: the predicates that are defined in the domain.
        :param domain_constants: the domains that might exist in the domain.
        """
        self.logger.debug("Parsing effects node.")
        self.effects_parser.parse(
            effects_ast,
            new_action,
            domain_types,
            domain_functions,
            domain_predicates,
            domain_constants,
        )

    def parse_action(
        self,
        action_ast: List[Union[str, List[str]]],
        domain_types: Dict[str, PDDLType],
        domain_functions: Dict[str, PDDLFunction],
        domain_predicates: Dict[str, Predicate],
        domain_constants: Dict[str, PDDLConstant] = {},
    ) -> Action:
        """Parse a single action AST and returns the object that represent a single action.

        :param action_ast: the AST representation of the action.
        :param domain_types: the types that were extracted from the domain.
        :param domain_functions: the functions that were extracted from the AST.
        :param domain_predicates: the predicates that were extracted from the domain's AST.
        :param domain_constants: the constants that might exist in the domain and might appear in the
            preconditions / effects.
        :return: the action object that is generated using the data from the domain AST.
        """
        self.logger.info("Starting to parse a new action!")
        new_action = Action()
        new_action.name = action_ast[0].lower()
        if len(action_ast[1:]) != 6:  # the number of different sections for the action.
            raise SyntaxError(
                f"Received an Illegal action AST definition! The action given - {action_ast}"
            )

        action_section_iterator = iter(action_ast[1:])
        for action_label_item in action_section_iterator:
            if action_label_item == ":parameters":
                self.logger.debug(
                    f"Parsing the parameters of the action - {new_action.name}"
                )
                parameters_list = next(action_section_iterator)
                new_action.signature = parse_signature(
                    iter(parameters_list), domain_types
                )
                continue

            if action_label_item == ":precondition" and not self.partial_parsing:
                self.logger.debug(
                    f"Starting to parse the preconditions of the action - {new_action.name}"
                )
                self.parse_preconditions(
                    next(action_section_iterator),
                    new_action,
                    domain_functions,
                    domain_predicates,
                    domain_types,
                    domain_constants,
                )
                continue

            if action_label_item == ":effect" and not self.partial_parsing:
                self.logger.debug(
                    f"Starting to parse the effects of the action - {new_action.name}"
                )
                self.parse_effects(
                    next(action_section_iterator),
                    new_action,
                    domain_types,
                    domain_functions,
                    domain_predicates,
                    domain_constants,
                )

        return new_action

    def parse_domain(self) -> Domain:
        """The main entry point that parses the domain file and returns the resulting Domain object.

        :return: the domain object extracted from the tokens.
        """
        domain_expressions = self.tokenizer.parse()
        if domain_expressions[0] != "define":
            raise SyntaxError(
                "Encountered a PDDL that does not start with 'define' statement!"
            )

        domain = Domain()
        for expression in domain_expressions[1:]:
            if expression[0] == "domain":
                domain.name = expression[1]

            elif expression[0] == ":requirements":
                domain.requirements = set(expression[1:])

            elif expression[0] == ":types":
                domain.types = self.parse_types(expression[1:])

            elif expression[0] == ":constants":
                domain.constants = self.parse_constants(expression[1:], domain.types)

            elif expression[0] == ":predicates":
                domain.predicates = self.parse_predicates(expression[1:], domain.types)

            elif expression[0] == ":functions":
                domain.functions = self.parse_functions(expression[1:], domain.types)

            elif expression[0] == ":action":
                new_action: Action = self.parse_action(
                    expression[1:],
                    domain.types,
                    domain.functions,
                    domain.predicates,
                    domain.constants,
                )
                domain.actions[new_action.name] = new_action

            elif expression[0] == ":process" or expression[0] == ":event":
                self.logger.debug("Still no support for temporal domains.")
                # TODO: complete once I finish numeric actions support

        return domain
