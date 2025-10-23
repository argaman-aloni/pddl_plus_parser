import itertools
import logging
from collections import defaultdict
from itertools import permutations
from typing import List, Tuple, Dict, Set, Union, Optional

from pddl_plus_parser.models.action_call import ActionCall
from pddl_plus_parser.models.pddl_action import Action
from pddl_plus_parser.models.pddl_domain import Domain
from pddl_plus_parser.models.pddl_function import PDDLFunction
from pddl_plus_parser.models.pddl_object import PDDLObject
from pddl_plus_parser.models.pddl_predicate import Predicate, GroundedPredicate
from pddl_plus_parser.models.pddl_type import PDDLType


def choose_objects_subset(array: List[str], subset_size: int) -> List[Tuple[str]]:
    """Choose r items our of a list size n.

    :param array: the input list.
    :param subset_size: the size of the subset.
    :return: a list containing subsets of the original list.
    """
    return list(permutations(array, subset_size))


class VocabularyCreator:
    """Creates predicate vocabulary from a domain containing action signatures and predicate definitions."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _validate_type_matching(
        self, grounded_signatures: Dict[str, PDDLType], lifted_variable_to_match: Union[Predicate, PDDLFunction, Action]
    ) -> bool:
        """Validates that the types of the grounded signature match the types of the predicate signature.

        :param grounded_signatures: the grounded predicate signature.
        :param lifted_variable_to_match: the lifted predicate.
        :return: whether the types match.
        """

        if len(grounded_signatures) != len(lifted_variable_to_match.signature):
            self.logger.debug(
                f"The number of objects - {grounded_signatures} does not match {lifted_variable_to_match.name}"
            )
            return False

        for object_name, predicate_parameter in zip(grounded_signatures, lifted_variable_to_match.signature):
            parameter_type = lifted_variable_to_match.signature[predicate_parameter]
            grounded_type = grounded_signatures[object_name]
            if not grounded_type.is_sub_type(parameter_type):
                self.logger.debug(
                    f"The combination of objects - {grounded_signatures}"
                    f" does not fit {lifted_variable_to_match.name}'s signature"
                )
                return False

        return True

    def create_grounded_predicate_vocabulary(
        self, domain: Domain, observed_objects: Dict[str, PDDLObject]
    ) -> Dict[str, Set[GroundedPredicate]]:
        """Create a vocabulary of random combinations of the predicates parameters and objects.

        :param domain: the domain containing the predicates and the action signatures.
        :param observed_objects: the objects that were observed in the trajectory.
        :return: list containing all the predicates with the different combinations of parameters.
        """
        vocabulary = defaultdict(set)
        possible_objects_str = list(observed_objects.keys()) + list(domain.constants.keys())
        objects_and_consts = list(observed_objects.values()) + list(domain.constants.values())
        for predicate in domain.predicates.values():
            predicate_name = predicate.name
            signature_permutations = choose_objects_subset(possible_objects_str, len(predicate.signature))
            for signature_permutation in signature_permutations:
                grounded_signature = {
                    object_name: objects_and_consts[possible_objects_str.index(object_name)].type
                    for object_name in signature_permutation
                }
                if not self._validate_type_matching(grounded_signature, predicate):
                    continue

                matching_grounded_type_hierarchy_signature = {
                    parameter_name: objects_and_consts[possible_objects_str.index(object_name)].type
                    for object_name, parameter_name in zip(grounded_signature, predicate.signature)
                }
                grounded_predicate = GroundedPredicate(
                    name=predicate_name,
                    signature=matching_grounded_type_hierarchy_signature,
                    object_mapping={
                        parameter_name: object_name
                        for object_name, parameter_name in zip(grounded_signature, predicate.signature)
                    },
                )
                vocabulary[predicate.untyped_representation].add(grounded_predicate)

        return vocabulary

    def create_lifted_functions_vocabulary(
        self, domain: Domain, possible_parameters: Dict[str, PDDLType], must_be_parameter: Optional[str] = None
    ) -> Dict[str, PDDLFunction]:
        """Create a function vocabulary from a domain containing action signatures and function definitions.

        :param domain: the domain containing the functions and the action signatures.
        :param possible_parameters: the parameters to use to create the vocabulary from.
        :param must_be_parameter: the parameter that must be in the function signature.
        :return: the vocabulary of functions.
        """
        self.logger.debug(f"Creating a function vocabulary from {possible_parameters}")
        vocabulary = {}
        possible_parameters_names = list(possible_parameters.keys()) + list(domain.constants.keys())
        parameter_types = list(possible_parameters.values()) + [const.type for const in domain.constants.values()]
        for predicate in domain.functions.values():
            function_name = predicate.name
            signature_permutations = choose_objects_subset(possible_parameters_names, len(predicate.signature))
            for signature_permutation in signature_permutations:
                bounded_lifted_signature = {
                    param_name: parameter_types[possible_parameters_names.index(param_name)]
                    for param_name in signature_permutation
                }

                if not self._validate_type_matching(bounded_lifted_signature, predicate):
                    continue

                if must_be_parameter and must_be_parameter not in bounded_lifted_signature:
                    continue

                lifted_function = PDDLFunction(name=function_name, signature=bounded_lifted_signature)
                vocabulary[lifted_function.untyped_representation] = lifted_function

        self.logger.debug(f"Created a lifted function vocabulary of size {len(vocabulary)}")
        return vocabulary

    def create_lifted_predicate_vocabulary(
        self, domain: Domain, possible_parameters: Dict[str, PDDLType], must_be_parameter: Optional[str] = None
    ) -> Set[Predicate]:
        """Create a vocabulary of random combinations of parameters that match the predicates.

        :param domain: the domain containing the predicates and the action signatures.
        :param possible_parameters: the parameters to use to create the vocabulary from.
        :param must_be_parameter: if not None, the vocabulary will only contain predicates that have this parameter.
        :return: list containing all the predicates with the different combinations of parameters.
        """
        self.logger.debug(f"Creating predicates vocabulary from {possible_parameters}")
        vocabulary = set()
        possible_parameters_names = list(possible_parameters.keys()) + list(domain.constants.keys())
        parameter_types = list(possible_parameters.values()) + [const.type for const in domain.constants.values()]
        for predicate in domain.predicates.values():
            predicate_name = predicate.name
            signature_permutations = choose_objects_subset(possible_parameters_names, len(predicate.signature))
            for signature_permutation in signature_permutations:
                bounded_lifted_signature = {
                    param_name: parameter_types[possible_parameters_names.index(param_name)]
                    for param_name in signature_permutation
                }

                if not self._validate_type_matching(bounded_lifted_signature, predicate):
                    continue

                if must_be_parameter and must_be_parameter not in bounded_lifted_signature:
                    continue

                lifted_predicate = Predicate(name=predicate_name, signature=bounded_lifted_signature)
                negative_lifted_predicate = lifted_predicate.copy()
                negative_lifted_predicate.is_positive = False
                vocabulary.update({lifted_predicate, negative_lifted_predicate})

        self.logger.debug(f"Created vocabulary of size {len(vocabulary)}")
        return vocabulary

    def create_grounded_actions_vocabulary(
        self, domain: Domain, observed_objects: Dict[str, PDDLObject]
    ) -> Set[ActionCall]:
        """Create a vocabulary of random combinations of the actions parameters and objects.

        :param domain: the domain containing the actions and the action signatures.
        :param observed_objects: the objects that were observed in the trajectory.
        :return: list containing all the actions with the different combinations of parameters.
        """
        vocabulary = set()
        objects_and_consts = list(observed_objects.values()) + list(domain.constants.values())
        for action_name, action in domain.actions.items():
            possible_objects_for_parameters = {
                parameter_name: [obj for obj in objects_and_consts if obj.type.is_sub_type(parameter_type)]
                for parameter_name, parameter_type in action.signature.items()
            }
            signature_options = list(itertools.product(*possible_objects_for_parameters.values()))
            for signature_option in signature_options:
                grounded_action = ActionCall(
                    name=action_name, grounded_parameters=[obj.name for obj in signature_option]
                )
                self.logger.debug(f"Created grounded action {str(grounded_action)}")
                vocabulary.add(grounded_action)

        return vocabulary
