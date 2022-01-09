"""Module that contains the parser for PDDL+ domain files."""
from pathlib import Path
from typing import List, Dict

from lisp_parsers import PDDLTokenizer
from models import Domain, PDDLType, Predicate, PDDLConstant, PDDLFunction

ObjectType = PDDLType(name="object", parent=None)


class DomainParser:
    """Class that parses PDDL+ domain files."""

    tokenizer: PDDLTokenizer

    def __init__(self, domain_path: Path):
        self.tokenizer = PDDLTokenizer(domain_path)

    def parse_types(self, types: List[str]) -> Dict[str, PDDLType]:
        """Parse the types of the domain.

        :param types: the list containing the
        :return: a mapping between the type name and the appropriate PDDLType object.
        """
        pddl_types = {}
        same_types_objects = []
        parent_types = {}
        found_parent_type = False
        for pddl_type in types:
            if found_parent_type:
                if pddl_type == "object":
                    parent_type = ObjectType
                elif pddl_type in parent_types:
                    parent_type = parent_types[pddl_type]
                else:
                    parent_type = PDDLType(name=pddl_type, parent=ObjectType)

                for descendant_type in same_types_objects:
                    new_type = PDDLType(name=descendant_type, parent=parent_type)
                    pddl_types[descendant_type] = new_type

                same_types_objects = []
                found_parent_type = False

            if type == "-":
                found_parent_type = True
                continue

            same_types_objects.append(pddl_type)

        return pddl_types

    def parse_constants(self, constants_ast: List[str], domain_types: Dict[str, PDDLType]) -> List[PDDLConstant]:
        """Parses the constants that appear in the constants part of the domain AST.

        :param constants_ast: the constants that were parsed in the domain AST.
        :param domain_types: the types that exist in the domain.
        :return: a list containing all typed constants.
        """
        constants = []
        same_type_constants = []
        type_marker_reached = False
        for constant_name in constants_ast:
            if type_marker_reached:
                # This means that the name of the constant here is actually its type.
                constants.extend([PDDLConstant(name, domain_types[constant_name]) for name in same_type_constants])
                type_marker_reached = False
                same_type_constants = []
                continue

            if constant_name == "-":
                type_marker_reached = True
                continue

            same_type_constants.append(constant_name)

        return constants

    def parse_predicates(self, predicates_ast: List[List[str]],
                         domain_types: Dict[str, PDDLType]) -> Dict[str, Predicate]:
        """Parses the predicates that appear in the predicates parsed AST.

        :param predicates_ast: the AST that contains the predicates of the domain.
        :param domain_types: the types that exist in the domain.
        :return: a mapping between the predicate name and the predicate itself.
        """
        predicates = {}
        for predicate in predicates_ast:
            predicate_name = predicate[0]
            if (len(predicate[1:]) % 2) != 0:
                raise StopAsyncIteration(f"Received a predicate with a wrong signature - {predicate[1:]}")

            signature_items = iter(predicate[1:])
            predicate_signature = {}
            for parameter_name in signature_items:
                parameter_type = next(signature_items)
                predicate_signature[parameter_name] = domain_types[parameter_type]

            predicates[predicate_name] = Predicate(name=predicate_name, signature=predicate_signature)

        return predicates

    def parse_functions(self, functions_ast: List[List[str]],
                        domain_types: Dict[str, PDDLType]) -> Dict[str, PDDLFunction]:
        """Parses the functions that appear in the functions parsed AST.

        :param functions_ast: the AST that contains the numerical functions of the domain.
        :param domain_types: the types that exist in the domain.
        :return: a mapping between a function name and the function itself.
        """
        functions = {}
        for function_items in functions_ast:
            function_name = function_items[0]
            if (len(function_items[1:]) % 2) != 0:
                raise StopAsyncIteration(f"Received a function with a wrong signature - {function_items[1:]}")

            signature_items = iter(function_items[1:])
            function_signature = {}
            for parameter_name in signature_items:
                parameter_type = next(signature_items)
                function_signature[parameter_name] = domain_types[parameter_type]

            functions[function_name] = PDDLFunction(name=function_name, signature=function_signature)

        return functions


    def parse_domain(self) -> Domain:
        """The main entry point that parses the domain file and returns the resulting Domain object.

        :return: the domain object extracted from the tokens.
        """
        domain_expressions = self.tokenizer.parse()
        if domain_expressions[0] != "define":
            raise SyntaxError("Encountered a PDDL that does not start with 'define' statement!")

        domain = Domain()
        for expression in domain_expressions[1:]:
            if expression[0] == "domain":
                domain.name = expression[1]

            elif expression[0] == ":requirements":
                domain.requirements = expression[1:]

            elif expression[0] == ":types":
                domain.types = self.parse_types(expression[1:])

            elif expression[0] == ":constants":
                domain.constants = self.parse_constants(expression[1:])

            elif expression[0] == ":predicates":
                domain.predicates = self.parse_predicates(expression[1:], domain.types)

            elif expression[0] == ":functions":
                domain.predicates = self.parse_functions(expression[1:], domain.types)
        #         elif element[0] == ":process":
        #             process = self.parse_world_change(element, WorldChangeTypes.process)
        #             domain.processes.append(process)
        #         elif element[0] == ":event":
        #             event = self.parse_world_change(element, WorldChangeTypes.event)
        #             domain.events.append(event)
        #         elif element[0] == ":action":
        #             action = self.parse_world_change(element, WorldChangeTypes.action)
        #             domain.actions.append(action)

        return domain


