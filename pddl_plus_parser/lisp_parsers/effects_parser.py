"""Module that handles parsing effects."""

import logging
from typing import List, Union, Dict

from pddl_plus_parser.lisp_parsers.parsing_utils import parse_untyped_predicate, \
    ASSIGNMENT_OPS, WHEN_OPERATOR, FORALL_OPERATOR, NOT_OPERATOR
from pddl_plus_parser.lisp_parsers.pddl_tokenizer import PDDLTokenizer
from pddl_plus_parser.lisp_parsers.preconditions_parser import PreconditionsParser
from pddl_plus_parser.models import PDDLFunction, Predicate, PDDLConstant, SignatureType, construct_expression_tree, \
    NumericalExpressionTree, PDDLType, Action, \
    CompoundPrecondition, ConditionalEffect, UniversalEffect


class EffectsParser:
    """Class to handle the functionality of parsing PDDL+ effects and compling them into objects."""

    tokenizer: PDDLTokenizer
    logger: logging.Logger

    def __init__(self, tokenizer: PDDLTokenizer):
        self.tokenizer = tokenizer
        self.preconditions_parser = PreconditionsParser(tokenizer)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _parse_result(action_signature: SignatureType, conditional_effect_ast: List[Union[str, List[str]]],
                      domain_constants: Dict[str, PDDLConstant],
                      domain_functions: Dict[str, PDDLFunction]) -> Union[Predicate, NumericalExpressionTree]:
        """

        :param action: the action that is being parsed.
        :param conditional_effect_ast: the AST representation of the conditional effect.
        :param domain_constants: the constants that exist in the domain.
        :param domain_functions: the functions that exist in the domain.
        """

        if conditional_effect_ast[0] == NOT_OPERATOR:
            return parse_untyped_predicate(conditional_effect_ast[1], action_signature, domain_constants, False)

        if conditional_effect_ast[0] in ASSIGNMENT_OPS:
            return NumericalExpressionTree(construct_expression_tree(conditional_effect_ast, domain_functions))

        return parse_untyped_predicate(conditional_effect_ast, action_signature, domain_constants, True)

    def _construct_conditional_effects(
            self, conditional_effect_ast: List[Union[str, List[str]]],
            antecedents: CompoundPrecondition,
            action_signature: SignatureType,
            domain_functions: Dict[str, PDDLFunction],
            domain_constants: Dict[str, PDDLConstant]) -> ConditionalEffect:
        """Parse all the conditional effects that are under the same when statement - can be composite.

        :param conditional_effect_ast: the AST representation of the conditional effects.
        :param action: the action that is being parsed.
        :param domain_functions: the functions that exist in the domain.
        :param domain_constants: the constants that exist in the domain.
        """
        discrete_effects = []
        numeric_effects = []
        if conditional_effect_ast[0] == "and":
            for effect in conditional_effect_ast[1:]:
                result = self._parse_result(action_signature, effect, domain_constants, domain_functions)
                if isinstance(result, Predicate):
                    discrete_effects.append(result)
                else:
                    numeric_effects.append(result)

        else:
            result = self._parse_result(action_signature, conditional_effect_ast, domain_constants, domain_functions)
            if isinstance(result, Predicate):
                discrete_effects.append(result)
            else:
                numeric_effects.append(result)

        conditional_effect = ConditionalEffect()
        conditional_effect.antecedents = antecedents
        conditional_effect.discrete_effects = set(discrete_effects)
        conditional_effect.numeric_effects = set(numeric_effects)
        return conditional_effect

    def parse_conditional_effect(
            self, conditional_effect_ast: List[Union[str, List[str]]], action_signature: SignatureType,
            domain_functions: Dict[str, PDDLFunction],
            domain_constants: Dict[str, PDDLConstant],
            domain_predicates: Dict[str, Predicate],
            domain_types: Dict[str, PDDLType]) -> ConditionalEffect:
        """Parse a conditional effect of an action.

        :param conditional_effect_ast: the AST representation of the conditional effect.
        :param action: the action that is being parsed.
        :param domain_functions: the functions that exist in the domain.
        :param domain_constants: the constants that exist in the domain.
        """
        self.logger.debug("Parsing conditional effect node.")
        if len(conditional_effect_ast[1:]) != 2:
            raise SyntaxError(f"Conditional effect scheme does not match schema! {conditional_effect_ast}")

        effect_antecedents = CompoundPrecondition()
        if conditional_effect_ast[1][0] == "and":
            antecedents_ast = conditional_effect_ast[1][1:]
        else:
            antecedents_ast = [conditional_effect_ast[1]]

        self.preconditions_parser.parse(precondition_root=effect_antecedents.root,
                                        preconditions_ast=antecedents_ast,
                                        domain_functions=domain_functions,
                                        domain_types=domain_types,
                                        domain_predicates=domain_predicates, domain_constants=domain_constants,
                                        action_signature=action_signature)

        conditional_effect = self._construct_conditional_effects(
            conditional_effect_ast[2], effect_antecedents, action_signature, domain_functions, domain_constants)
        return conditional_effect

    def parse_universally_quantified_effect(
            self, universal_quantifier_ast: List[Union[str, List[str]]],
            action: Action,
            domain_types: Dict[str, PDDLType],
            domain_predicates: Dict[str, Predicate],
            domain_functions: Dict[str, PDDLFunction],
            domain_constants: Dict[str, PDDLConstant]) -> UniversalEffect:
        """Parse a universally quantified effect of an action.

        :param domain_predicates:
        :param universal_quantifier_ast: the ast representation of the universally quantified effect.
        :param action: the action that is being parsed.
        :param domain_types: the types that exist in the domain.
        :param domain_functions: the functions that exist in the domain.
        :param domain_constants: the constants that exist in the domain.
        """
        self.logger.debug("Parsing universally quantified effect node.")
        if len(universal_quantifier_ast) != 2:
            raise SyntaxError(f"Universal quantifier scheme does not match for action {action.name}!")

        quantified_object_components = universal_quantifier_ast[0]
        # quantified object components are of the form ( ?x - type )
        if len(quantified_object_components) != 3:
            raise SyntaxError(f"Quantified object scheme does not match for action {action.name}!"
                              f"Expected 3 components, got {len(quantified_object_components)}!")

        quantified_param = quantified_object_components[0]
        quantified_type = domain_types[quantified_object_components[2]]
        extended_signature = {**action.signature, quantified_param: quantified_type}

        conditional_effect_ast = universal_quantifier_ast[1]
        conditional_effect = self.parse_conditional_effect(
            conditional_effect_ast, extended_signature,
            domain_functions, domain_constants, domain_predicates, domain_types)

        universal_effect = UniversalEffect(quantified_parameter=quantified_param, quantified_type=quantified_type)
        universal_effect.conditional_effects.add(conditional_effect)
        return universal_effect

    def parse(self, effects_ast: List[Union[str, List[str]]],
              new_action: Action,
              domain_types: Dict[str, PDDLType],
              domain_functions: Dict[str, PDDLFunction],
              domain_predicates: Dict[str, Predicate],
              domain_constants: Dict[str, PDDLConstant]) -> None:
        """Parse the effects of a single action.

        :param effects_ast: the AST representation of the action's effects.
        :param new_action: the action that is currently being parsed.
        :param domain_types: the types that exist in the domain.
        :param domain_functions: the functions that exist in the domain.
        :param domain_predicates: the predicates that are defined in the domain.
        :param domain_constants: the domains that might exist in the domain.
        """
        new_action.discrete_effects = set()
        new_action.numeric_effects = set()
        if effects_ast[0] != "and":
            raise SyntaxError(
                f"Only accepting conjunctive effects! Action - {new_action.name} does not conform!")

        for effect_node in effects_ast[1:]:
            if effect_node[0] in domain_predicates:
                new_action.discrete_effects.add(
                    parse_untyped_predicate(effect_node, new_action.signature, domain_constants, is_positive=True))
                continue

            if effect_node[0] == NOT_OPERATOR:
                new_action.discrete_effects.add(
                    parse_untyped_predicate(effect_node[1], new_action.signature, domain_constants, is_positive=False))
                continue

            if effect_node[0] == FORALL_OPERATOR:
                new_action.universal_effects.add(
                    self.parse_universally_quantified_effect(
                        effect_node[1:], new_action, domain_types, domain_predicates, domain_functions,
                        domain_constants))
                continue

            if effect_node[0] == WHEN_OPERATOR:
                new_action.conditional_effects.add(
                    self.parse_conditional_effect(effect_node, new_action.signature, domain_functions,
                                                  domain_constants, domain_predicates, domain_types))
                continue

            if effect_node[0] in ASSIGNMENT_OPS:
                numerical_precondition = NumericalExpressionTree(
                    construct_expression_tree(effect_node, domain_functions))
                new_action.numeric_effects.add(numerical_precondition)
                continue
