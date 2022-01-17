"""Module containing utility functionality for the parsing process."""
from collections import Iterator
from typing import Dict

from models import PDDLType, SignatureType


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