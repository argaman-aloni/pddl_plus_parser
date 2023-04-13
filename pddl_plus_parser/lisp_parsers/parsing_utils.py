"""Module containing utility functionality for the parsing process."""
from typing import Dict, Iterator, List

from pddl_plus_parser.models import PDDLType, SignatureType, Predicate, PDDLConstant, Action


COMPARISON_OPS = ["<=", ">=", ">", "<"]
BINARY_OPERATORS = ["and", "or"]
EQUALITY_OPERATOR = "="
NOT_OPERATOR = "not"
FORALL_OPERATOR = "forall"
ASSIGNMENT_OPS = ["assign", "increase", "decrease"]
WHEN_OPERATOR = "when"

def parse_signature(parameters: Iterator[str], domain_types: Dict[str, PDDLType]) -> SignatureType:
    """Parse the signature of a statement.

    :param parameters: the parameters that appear in the signature.
    :param domain_types: the types that were extracted from the domain.
    :return: the object representing the signature's data.
    """
    signature = {}
    for parameter_name in parameters:
        # now the next item is the dash that we need to ignore
        next(parameters)
        parameter_type = next(parameters)
        signature[parameter_name] = domain_types[parameter_type]

    return signature


def parse_untyped_predicate(untyped_predicate: List[str], action_signature: SignatureType,
                            domain_constants: Dict[str, PDDLConstant] = {}, is_positive: bool = True) -> Predicate:
    """Parse an untyped predicate that appears in actions.

    :param untyped_predicate: the untyped predicate that needs to be matched to the typed predicate from the
        predicates definitions.
    :param action_signature: the signed signature of the action.
    :return: the predicate including the relevant types.
    :param domain_constants: the constants that are defined in the domain.
    """
    predicate_name = untyped_predicate[0]
    possible_signed_objects = {key: val for key, val in action_signature.items()}
    possible_signed_objects.update({const_name: const.type for const_name, const in domain_constants.items()})
    # Since we assume that the order in maintained in the predicates we can match the signatures.
    signed_signature = {parameter_name: possible_signed_objects[parameter_name] for
                        parameter_name in untyped_predicate[1:]}

    return Predicate(name=predicate_name, signature=signed_signature, is_positive=is_positive)


def extend_action_to_contain_quantified_objects(
        action: Action, quantified_param: str, quantified_type: PDDLType) -> Action:
    """Extends the relevant parts of the action to include the quantified object.

    :param action: the action to extend.
    :param quantified_param: the name of the parameter that is added to the extended action.
    :param quantified_type: the type of the quantified object.
    :return: the extended action.
    """
    combined_signature = {**action.signature, quantified_param: quantified_type}
    extended_action = Action()
    extended_action.name = action.name
    extended_action.signature = combined_signature
    return extended_action
