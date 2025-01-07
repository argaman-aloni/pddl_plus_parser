"""Module containing utility functionality for the parsing process."""
from typing import Dict, Iterator, List

from pddl_plus_parser.lisp_parsers import PDDLTokenizer
from pddl_plus_parser.models import PDDLType, SignatureType, Predicate, PDDLConstant, ObjectType

COMPARISON_OPS = ["<=", ">=", ">", "<"]
BINARY_OPERATORS = ["and", "or"]
EQUALITY_OPERATOR = "="
NOT_OPERATOR = "not"
FORALL_OPERATOR = "forall"
ASSIGNMENT_OPS = ["assign", "increase", "decrease"]
WHEN_OPERATOR = "when"

PARAMETERS_INVALID_SYNTAX_ERROR = "The parameters should start with a question mark."


def parse_signature(parameters: Iterator[str], domain_types: Dict[str, PDDLType]) -> SignatureType:
    """Parse the signature of a statement.

    :param parameters: the parameters that appear in the signature.
    :param domain_types: the types that were extracted from the domain.
    :return: the object representing the signature's data.
    """
    # For each group of parameters (possibly of size one) search for the dash that indicates the type of the parameter.
    # If the dash does noe exist, assign the default type of object.
    # Then, try to find the next set of parameters.
    signature = {}
    grouped_params = []
    for parameter in parameters:
        if parameter == "-":
            parameter_type = next(parameters)
            if any([not param.startswith("?") for param in grouped_params]):
                raise SyntaxError(PARAMETERS_INVALID_SYNTAX_ERROR)

            for grouped_param in grouped_params:
                signature[grouped_param] = domain_types[parameter_type]

            grouped_params = []

        else:
            if not parameter.startswith("?"):
                raise SyntaxError(PARAMETERS_INVALID_SYNTAX_ERROR)

            grouped_params.append(parameter)

    if len(grouped_params) > 0:
        for param in grouped_params:
            signature[param] = ObjectType

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


def parse_predicate_from_string(predicate_str: str, types_map: Dict[str, PDDLType]) -> Predicate:
    """Creates a predicate object from a string representation.

    Notice: currently supporting predicates string in the form:
        (predicate_name ?param1 - type1 ?param2 - type2 ...)

    :param predicate_str: the string representation of the predicate.
    :param types_map: the map of types that are used in the domain.
    :return: the predicate object.
    """
    tokenizer = PDDLTokenizer(pddl_str=predicate_str)
    expression = tokenizer.parse()
    predicate_name = expression[0]
    signature_items = iter(expression[1:])
    predicate_signature = parse_signature(signature_items, types_map)
    extracted_predicate = Predicate(name=predicate_name, signature=predicate_signature, is_positive=True)
    return extracted_predicate