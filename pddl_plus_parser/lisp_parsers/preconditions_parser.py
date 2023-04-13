"""class to handle the functionality of parsing PDDL+ preconditions and compling them into Precondition objects."""
import logging
from typing import List, Union, Dict, Optional

from pddl_plus_parser.lisp_parsers.parsing_utils import parse_untyped_predicate, BINARY_OPERATORS, EQUALITY_OPERATOR, \
    COMPARISON_OPS, FORALL_OPERATOR, NOT_OPERATOR
from pddl_plus_parser.lisp_parsers.pddl_tokenizer import PDDLTokenizer
from pddl_plus_parser.models import PDDLFunction, Predicate, PDDLConstant, Precondition, \
    SignatureType, construct_expression_tree, NumericalExpressionTree, UniversalPrecondition, PDDLType


class PreconditionsParser:
    """Class to handle the functionality of parsing PDDL+ preconditions and compling them into Precondition objects."""

    tokenizer: PDDLTokenizer
    logger: logging.Logger

    def __init__(self, tokenizer: PDDLTokenizer):
        self.tokenizer = tokenizer
        self.logger = logging.getLogger(__name__)

    def parse(self, precondition_root: Union[Precondition, UniversalPrecondition],
              preconditions_ast: List[Union[str, List[str]]],
              domain_functions: Dict[str, PDDLFunction],
              domain_predicates: Dict[str, Predicate],
              domain_types: Dict[str, PDDLType],
              domain_constants: Dict[str, PDDLConstant],
              action_signature: SignatureType) -> Optional[Precondition]:
        """Parse the token stream and return a Precondition object."""
        for precondition_node in preconditions_ast:
            if precondition_node[0] in BINARY_OPERATORS:
                nested_precondition = Precondition(precondition_node[0])
                precondition_root.add_condition(
                    self.parse(nested_precondition, precondition_node[1:], domain_functions, domain_predicates,
                               domain_types, domain_constants, action_signature))
                continue

            if precondition_node[0] in domain_predicates:
                precondition_root.add_condition(
                    parse_untyped_predicate(precondition_node, action_signature, domain_constants, is_positive=True))
                continue

            if precondition_node[0] == NOT_OPERATOR:
                inner_node = precondition_node[1]
                if inner_node[0] == EQUALITY_OPERATOR:
                    self.logger.debug("Adding new lifted objects that should be tested for inequality")
                    precondition_root.inequality_preconditions.add((inner_node[1], inner_node[2]))
                    continue

                # no support on not for compound logical expressions
                precondition_root.add_condition(
                    parse_untyped_predicate(inner_node, action_signature, domain_constants, is_positive=False))
                continue

            if precondition_node[0] == EQUALITY_OPERATOR:
                if isinstance(precondition_node[1], List):
                    self.logger.debug("Found numeric equality precondition")
                    numeric_precondition = NumericalExpressionTree(construct_expression_tree(
                        precondition_node, domain_functions))
                    precondition_root.add_condition(numeric_precondition)
                    continue

                self.logger.debug("Adding new lifted objects that should be tested for equality")
                precondition_root.equality_preconditions.add((precondition_node[1], precondition_node[2]))
                continue

            if precondition_node[0] in COMPARISON_OPS:
                numeric_precondition = NumericalExpressionTree(
                    construct_expression_tree(precondition_node, domain_functions))
                precondition_root.add_condition(numeric_precondition)
                continue

            if precondition_node[0] == FORALL_OPERATOR:
                self.logger.debug("Found forall precondition")
                forall_ast = precondition_node[1:]
                quantified_object_components = forall_ast[0]
                if len(quantified_object_components) != 3:
                    raise SyntaxError(f"Quantified object scheme does not match schema of ( ?param - type )!"
                                      f"Expected 3 components, got {len(quantified_object_components)}!")

                quantified_conditions = forall_ast[1]
                if quantified_conditions[0] not in BINARY_OPERATORS:
                    raise SyntaxError(f"Quantified conditions must start with binary operator!")

                quantified_param_name = quantified_object_components[0]
                quantified_type = domain_types[quantified_object_components[2]]
                universal_precondition = UniversalPrecondition(
                    quantified_parameter=quantified_param_name, quantified_type=quantified_type,
                    binary_operator=quantified_conditions[0])

                combined_signature = {**action_signature, quantified_param_name: quantified_type}
                self.parse(universal_precondition, quantified_conditions[1:], domain_functions, domain_predicates,
                           domain_types, domain_constants, combined_signature)
                precondition_root.add_condition(universal_precondition)
                continue

            else:
                self.logger.error(f"Unknown precondition node: {precondition_node}")
                return None

        return precondition_root
