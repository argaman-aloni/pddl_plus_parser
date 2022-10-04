"""Module that contains the parser for PDDL+ domain files."""
import logging
import types
from pathlib import Path
from typing import List, Dict, Union, NoReturn, Tuple

from pddl_plus_parser.models import Domain, PDDLType, Predicate, PDDLConstant, PDDLFunction, Action, SignatureType, \
    NumericalExpressionTree, construct_expression_tree, ConditionalEffect
from .parsing_utils import parse_signature
from .pddl_tokenizer import PDDLTokenizer

ObjectType = PDDLType(name="object", parent=None)

COMPARISON_OPS = ["=", "<=", ">=", ">", "<"]
ASSIGNMENT_OPS = ["assign", "increase", "decrease"]
EQUALITY_OPERATOR = "="


class DomainParser:
    """Class that parses PDDL+ domain files."""

    tokenizer: PDDLTokenizer
    logger: logging.Logger
    partial_parsing: bool
    enable_conjunctions: bool

    def __init__(self, domain_path: Path, partial_parsing: bool = False, enable_conjunctions: bool = False):
        self.tokenizer = PDDLTokenizer(domain_path)
        self.logger = logging.getLogger(__name__)
        self.partial_parsing = partial_parsing
        self.enable_conjunctions = enable_conjunctions

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
            parent_type = pddl_types.get(pddl_type, PDDLType(name=pddl_type, parent=ObjectType))
            pddl_types.update({descendant_typ_name: PDDLType(name=descendant_typ_name, parent=parent_type)
                               for descendant_typ_name in same_types_objects})
            same_types_objects = []
            index += 2
            continue

        if len(same_types_objects) > 0:
            pddl_types.update({type_name: PDDLType(name=type_name, parent=ObjectType)
                               for type_name in same_types_objects})

        pddl_types["object"] = ObjectType
        self.logger.debug(f"Extracted {len(pddl_types)} types while parsing the types AST.")
        return pddl_types

    def parse_constants(self, constants_ast: List[str], domain_types: Dict[str, PDDLType]) -> Dict[str, PDDLConstant]:
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
                    {name: PDDLConstant(name, domain_types[constant_name]) for name in same_type_constants})
                type_marker_reached = False
                same_type_constants = []
                continue

            if constant_name == "-":
                type_marker_reached = True
                continue

            same_type_constants.append(constant_name)

        self.logger.debug(f"Extracted {len(constants)} from the domain.")
        return constants

    def parse_predicate(self, predicate: List[str], domain_types: Dict[str, PDDLType]) -> Predicate:
        """Parse a single predicate from an AST representation in the PDDL domain.

        :param predicates_ast: the predicate in the form of an AST list of strings.
        :param domain_types: the types that were extracted from the domain.
        :return: the predicate object that represents the list of strings that were given.
        """
        self.logger.info(f"Parsing the predicate represented by the AST - {predicate}")
        predicate_name = predicate[0]
        if (len(predicate[1:]) % 3) != 0:
            raise SyntaxError(f"Received a predicate with a wrong signature - {predicate[1:]}")

        signature_items = iter(predicate[1:])
        predicate_signature = parse_signature(signature_items, domain_types)
        extracted_predicate = Predicate(name=predicate_name, signature=predicate_signature)
        self.logger.debug(f"Finished extracting the predicate - {extracted_predicate}")
        return extracted_predicate

    def parse_untyped_predicate(self, untyped_predicate: List[str], action_signature: SignatureType,
                                domain_constants: Dict[str, PDDLConstant] = {}) -> Predicate:
        """Parse an untyped predicate that appears in actions.

        :param untyped_predicate: the untyped predicate that needs to be matched to the typed predicate from the
            predicates definitions.
        :param action_signature: the signed signature of the action.
        :return: the predicate including the relevant types.
        :param domain_constants: the constants that are defined in the domain.
        """
        self.logger.info(f"Parsing the untyped action predicate represented by the AST - {untyped_predicate}")
        predicate_name = untyped_predicate[0]
        possible_signed_objects = {key: val for key, val in action_signature.items()}
        possible_signed_objects.update({const_name: const.type for const_name, const in domain_constants.items()})
        # Since we assume that the order in maintained in the predicates we can match the signatures.
        signed_signature = {parameter_name: possible_signed_objects[parameter_name] for
                            parameter_name in untyped_predicate[1:]}

        signed_action_predicate = Predicate(name=predicate_name, signature=signed_signature)
        self.logger.debug(f"Extracted the predicate - {signed_action_predicate}")
        return signed_action_predicate

    def parse_predicates(self, predicates_ast: List[List[str]],
                         domain_types: Dict[str, PDDLType]) -> Dict[str, Predicate]:
        """Parses the predicates that appear in the predicates parsed AST.

        :param predicates_ast: the AST that contains the predicates of the domain.
        :param domain_types: the types that exist in the domain.
        :return: a mapping between the predicate name and the predicate itself.
        """
        predicates = {}
        for predicate in predicates_ast:
            if predicate[0] == ":private":
                for private_predicate in predicate[1:]:
                    extracted_private_predicate = self.parse_predicate(private_predicate, domain_types)
                    predicates[extracted_private_predicate.name] = extracted_private_predicate

                continue

            extracted_predicate = self.parse_predicate(predicate, domain_types)
            predicates[extracted_predicate.name] = extracted_predicate

        return predicates

    def parse_functions(self, functions_ast: List[List[str]],
                        domain_types: Dict[str, PDDLType]) -> Dict[str, PDDLFunction]:
        """Parses the functions that appear in the functions parsed AST.

        :param functions_ast: the AST that contains the numerical functions of the domain.
        :param domain_types: the types that exist in the domain.
        :return: a mapping between a function name and the function itself.
        """
        self.logger.info("Starting to parse the function' definition in the domain data.")
        functions = {}
        for function_items in functions_ast:
            function_name = function_items[0]
            if (len(function_items[1:]) % 3) != 0:
                raise SyntaxError(f"Received a function with a wrong signature - {function_items[1:]}")

            signature_items = iter(function_items[1:])
            function_signature = parse_signature(signature_items, domain_types)
            functions[function_name] = PDDLFunction(name=function_name, signature=function_signature)

        return functions

    def parse_disjunctive_numeric_preconditions(
            self, numeric_preconditions_node: List[Union[str, List[str]]],
            new_action: Action, domain_functions: Dict[str, PDDLFunction]) -> NoReturn:
        """Parse a set of disjunctive numeric preconditions.

        :param numeric_preconditions_node: the node that contains the numeric preconditions.
        :param new_action: the action that is currently being parsed.
        :param domain_functions: the functions that are defined in the domain.
        """
        self.logger.info("Starting to parse the disjunctive numeric preconditions!")
        for conditions_set_ast in numeric_preconditions_node:
            if conditions_set_ast[0] != "and":
                raise SyntaxError(
                    f"Only accepting conjunctive preconditions! Action - {new_action.name} does not conform!")

            conditions_set = {NumericalExpressionTree(construct_expression_tree(node, domain_functions)) for node in
                              conditions_set_ast[1:]}
            new_action.disjunctive_numeric_preconditions.append(conditions_set)

    def parse_preconditions(self, preconditions_ast: List[Union[str, List[str]]], new_action: Action,
                            domain_functions: Dict[str, PDDLFunction],
                            domain_predicates: Dict[str, Predicate],
                            domain_constants: Dict[str, PDDLConstant]) -> NoReturn:
        """Parse the preconditions of a single action.

        :param preconditions_ast: the AST representation of the action's preconditions.
        :param new_action: the action that is currently being parsed.
        :param domain_functions: the functions that exist in the domain.
        :param domain_predicates: the predicates that exist in the domain.
        :param domain_constants: the constants that might exist in the domain.
        """
        new_action.positive_preconditions = set()
        new_action.negative_preconditions = set()
        new_action.equality_preconditions = set()
        new_action.inequality_preconditions = set()
        new_action.numeric_preconditions = set()
        if len(preconditions_ast) == 0:
            self.logger.warning("Received an action with no preconditions.")
            return

        if preconditions_ast[0] != "and" and not self.enable_conjunctions:
            raise SyntaxError(f"Only accepting conjunctive preconditions! Action - {new_action.name} does not conform!")

        for precondition_node in preconditions_ast[1:]:
            if precondition_node[0] in domain_predicates:
                new_action.positive_preconditions.add(
                    self.parse_untyped_predicate(precondition_node, new_action.signature, domain_constants))
                continue

            if precondition_node[0] == "not":
                inner_node = precondition_node[1]
                if inner_node[0] == EQUALITY_OPERATOR:
                    self.logger.debug("Adding new lifted objects that should be tested for inequality")
                    new_action.inequality_preconditions.add((inner_node[1], inner_node[2]))
                    continue

                new_action.negative_preconditions.add(
                    self.parse_untyped_predicate(precondition_node[1], new_action.signature, domain_constants))
                continue

            if precondition_node[0] == EQUALITY_OPERATOR:
                if not isinstance(precondition_node[1], List):
                    self.logger.debug("Adding new lifted objects that should be tested for equality")
                    new_action.equality_preconditions.add((precondition_node[1], precondition_node[2]))
                    continue

            if precondition_node[0] == "or":
                self.logger.debug("Assuming that the OR operator is used for the disjunction of numeric preconditions.")
                self.parse_disjunctive_numeric_preconditions(precondition_node[1:], new_action, domain_functions)

            if precondition_node[0] in COMPARISON_OPS:
                numerical_precondition = NumericalExpressionTree(
                    construct_expression_tree(precondition_node, domain_functions))
                new_action.numeric_preconditions.add(numerical_precondition)
                continue

    def _parse_single_conditional(self, conditional: List[Union[str, List[str]]],
                                  positive_conditionals: List[Predicate], negative_conditionals: List[Predicate],
                                  numeric_conditionals: List[NumericalExpressionTree],
                                  signature: Dict[str, PDDLType], domain_functions: Dict[str, PDDLFunction],
                                  domain_constants: Dict[str, PDDLConstant]) -> NoReturn:
        """Parse a single conditional from the conditional effect.

        :param conditional: the single conditional effect to parse.
        :param positive_conditionals: the positive conditionals of the conditional effect to
            possibly add the conditional to.
        :param negative_conditionals: the negative conditionals of the conditional effect to
            possibly add the conditional to.
        :param numeric_conditionals: the numeric conditionals of the conditional effect.
        :param signature: the action's signature.
        :param domain_functions: the functions that exist in the domain.
        :param domain_constants: the constants that exist in the domain.
        """
        if conditional[0] == "not":
            negative_conditionals.append(
                self.parse_untyped_predicate(conditional[1], signature, domain_constants))

        elif conditional[0] in COMPARISON_OPS:
            numerical_precondition = NumericalExpressionTree(
                construct_expression_tree(conditional, domain_functions))
            numeric_conditionals.append(numerical_precondition)

        else:
            positive_conditionals.append(self.parse_untyped_predicate(conditional, signature, domain_constants))

    def _parse_conditionals(
            self, conditional_ast: List[Union[str, List[str]]],
            signature: Dict[str, PDDLType], domain_functions: Dict[str, PDDLFunction],
            domain_constants: Dict[str, PDDLConstant]) -> Tuple[
        List[Predicate], List[Predicate], List[NumericalExpressionTree]]:
        """Parse the conditionals for a conditional effect of an action.

        :param conditional_ast: the AST representation of the conditionals.
        :param signature: the action's signature.
        :param domain_functions: the functions that exist in the domain.
        :param domain_constants: the constants that exist in the domain.
        :return: a tuple containing the positive and negative and numeric conditionals (in this order).
        """
        positive_conditionals = []
        negative_conditionals = []
        numeric_conditionals = []
        if conditional_ast[0] == "and":
            self.logger.debug("Received a conjunctive conditional effect with more than one condition.")
            for conditional in conditional_ast[1:]:
                self._parse_single_conditional(conditional, positive_conditionals, negative_conditionals,
                                               numeric_conditionals, signature, domain_functions, domain_constants)

        else:
            self._parse_single_conditional(conditional_ast, positive_conditionals, negative_conditionals,
                                           numeric_conditionals, signature, domain_functions, domain_constants)

        return positive_conditionals, negative_conditionals, numeric_conditionals

    def _parse_single_conditional_effect(self, action, conditional_effect_ast, add_effects, del_effects,
                                         numeric_effects, domain_constants, domain_functions) -> NoReturn:
        """

        :param action: the action that is being parsed.
        :param conditional_effect_ast: the AST representation of the conditional effect.
        :param add_effects: the add effects of the action.
        :param del_effects: the delete effects of the action.
        :param numeric_effects: the numeric effects of the action.
        :param domain_constants: the constants that exist in the domain.
        :param domain_functions: the functions that exist in the domain.
        """

        if conditional_effect_ast[0] == "not":
            del_effects.append(
                self.parse_untyped_predicate(conditional_effect_ast[1], action.signature, domain_constants))

        elif conditional_effect_ast[0] in ASSIGNMENT_OPS:
            numeric_effects.append(
                NumericalExpressionTree(construct_expression_tree(conditional_effect_ast, domain_functions)))

        else:
            add_effects.append(self.parse_untyped_predicate(conditional_effect_ast, action.signature, domain_constants))

    def _construct_conditional_effects(self, conditional_effect_ast: List[Union[str, List[str]]],
                                       positive_conditionals: List[Predicate], negative_conditionals: List[Predicate],
                                       numeric_conditionals: List[NumericalExpressionTree],
                                       action: Action, domain_functions: Dict[str, PDDLFunction],
                                       domain_constants: Dict[str, PDDLConstant]) -> NoReturn:
        """Parse all the conditional effects that are under the same when statement - can be composite.

        :param conditional_effect_ast: the AST representation of the conditional effects.
        :param positive_conditionals: the positive conditionals of the conditional effect.
        :param negative_conditionals: the negative conditionals of the conditional effect.
        :param numeric_conditionals: the numeric conditionals of the conditional effect.
        :param action: the action that is being parsed.
        :param domain_functions: the functions that exist in the domain.
        :param domain_constants: the constants that exist in the domain.
        """
        add_effects = []
        del_effects = []
        numeric_effects = []
        if conditional_effect_ast[0] == "and":
            for effect in conditional_effect_ast[1:]:
                self._parse_single_conditional_effect(action, effect, add_effects, del_effects, numeric_effects,
                                                      domain_constants, domain_functions)

        else:
            self._parse_single_conditional_effect(action, conditional_effect_ast, add_effects, del_effects,
                                                  numeric_effects, domain_constants, domain_functions)

        conditional_effect = ConditionalEffect()
        conditional_effect.add_effects = set(add_effects)
        conditional_effect.delete_effects = set(del_effects)
        conditional_effect.numeric_effects = set(numeric_effects)
        conditional_effect.positive_conditions = set(positive_conditionals)
        conditional_effect.negative_conditions = set(negative_conditionals)
        conditional_effect.numeric_conditions = set(numeric_conditionals)
        action.conditional_effects.add(conditional_effect)

    def parse_effects(self, effects_ast: List[Union[str, List[str]]], new_action: Action,
                      domain_functions: Dict[str, PDDLFunction],
                      domain_predicates: Dict[str, Predicate],
                      domain_constants: Dict[str, PDDLConstant]) -> NoReturn:
        """Parse the effects of a single action.

        :param effects_ast: the AST representation of the action's effects.
        :param new_action: the action that is currently being parsed.
        :param domain_functions: the functions that exist in the domain.
        :param domain_predicates: the predicates that are defined in the domain.
        :param domain_constants: the domains that might exist in the domain.
        """
        new_action.add_effects = set()
        new_action.delete_effects = set()
        new_action.numeric_effects = set()
        if effects_ast[0] != "and":
            print(effects_ast[0])
            raise SyntaxError(
                f"Only accepting conjunctive effects! Action - {new_action.name} does not conform!")

        for effect_node in effects_ast[1:]:
            if effect_node[0] in domain_predicates:
                new_action.add_effects.add(
                    self.parse_untyped_predicate(effect_node, new_action.signature, domain_constants))
                continue

            if effect_node[0] == "not":
                new_action.delete_effects.add(
                    self.parse_untyped_predicate(effect_node[1], new_action.signature, domain_constants))
                continue

            if effect_node[0] == "when":
                if len(effect_node[1:]) != 2:
                    raise SyntaxError(f"Conditional effect scheme does not match for action {new_action.name}!")

                self.logger.debug("Found a conditional effect!")
                positive_conditionals, negative_conditionals, numerical_conditionals = \
                    self._parse_conditionals(effect_node[1], new_action.signature, domain_functions, domain_constants)

                self._construct_conditional_effects(effect_node[2], positive_conditionals, negative_conditionals,
                                                    numerical_conditionals, new_action, domain_functions,
                                                    domain_constants)

                continue

            if effect_node[0] in ASSIGNMENT_OPS:
                numerical_precondition = NumericalExpressionTree(
                    construct_expression_tree(effect_node, domain_functions))
                new_action.numeric_effects.add(numerical_precondition)
                continue

    def parse_action(self, action_ast: List[Union[str, List[str]]], domain_types: Dict[str, PDDLType],
                     domain_functions: Dict[str, PDDLFunction],
                     domain_predicates: Dict[str, Predicate],
                     domain_constants: Dict[str, PDDLConstant] = {}) -> Action:
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
            raise SyntaxError(f"Received an Illegal action AST definition! The action given - {action_ast}")

        action_section_iterator = iter(action_ast[1:])
        for action_label_item in action_section_iterator:
            if action_label_item == ":parameters":
                self.logger.debug(f"Parsing the parameters of the action - {new_action.name}")
                parameters_list = next(action_section_iterator)
                new_action.signature = parse_signature(iter(parameters_list), domain_types)
                continue

            if action_label_item == ":precondition" and not self.partial_parsing:
                self.logger.debug(f"Starting to parse the preconditions of the action - {new_action.name}")
                self.parse_preconditions(next(action_section_iterator), new_action, domain_functions,
                                         domain_predicates, domain_constants)
                continue

            if action_label_item == ":effect" and not self.partial_parsing:
                self.logger.debug(f"Starting to parse the effects of the action - {new_action.name}")
                self.parse_effects(next(action_section_iterator), new_action, domain_functions,
                                   domain_predicates, domain_constants)

        return new_action

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
                domain.constants = self.parse_constants(expression[1:], domain.types)

            elif expression[0] == ":predicates":
                domain.predicates = self.parse_predicates(expression[1:], domain.types)

            elif expression[0] == ":functions":
                domain.functions = self.parse_functions(expression[1:], domain.types)

            elif expression[0] == ":action":
                new_action: Action = self.parse_action(expression[1:], domain.types, domain.functions,
                                                       domain.predicates, domain.constants)
                domain.actions[new_action.name] = new_action

            elif expression[0] == ":process" or expression[0] == ":event":
                self.logger.debug("Still no support for temporal domains.")
                # TODO: complete once I finish numeric actions support

        return domain
