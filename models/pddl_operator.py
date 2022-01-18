"""module to represent an oprator that can apply actions and change state objects."""
from typing import List, Set, Dict

from models import Action, State, GroundedPredicate, NumericalExpressionTree, Domain, Predicate


class Operator:
    action: Action
    domain: Domain
    grounded_call_objects: List[str]

    # These fields are constructed after the grounding process.
    grounded_positive_preconditions: Set[GroundedPredicate]
    grounded_negative_preconditions: Set[GroundedPredicate]
    grounded_numeric_preconditions: Set[NumericalExpressionTree]
    grounded_add_effects: Set[GroundedPredicate]
    grounded_delete_effects: Set[GroundedPredicate]
    grounded_numeric_effects: Set[NumericalExpressionTree]

    def __init__(self, action: Action, domain: Domain, grounded_action_call: List[str]):
        self.action = action
        self.domain = domain
        self.grounded_call_objects = grounded_action_call

    def ground_predicates(self, lifted_predicates: Set[Predicate],
                          parameters_map: Dict[str, str]) -> Set[GroundedPredicate]:
        """

        :param lifted_predicates:
        :param parameters_map:
        :return:
        """
        output_grounded_predicates = set()
        for predicate in lifted_predicates:
            predicate_name = predicate.name
            predicate_signature = {param: param_type for param, param_type in
                                   self.domain.predicates[predicate_name].signature.items()}
            action_predicate_map = {predicate_item: action_item
                                    for predicate_item, action_item in zip(predicate_signature, self.action.signature)}

            # Matching the types to be the same as the ones in the action.
            predicate_object_binding = {}
            for parameter in predicate_signature:
                predicate_signature[parameter] = self.action.signature[action_predicate_map[parameter]]
                predicate_object_binding[parameter] = parameters_map[action_predicate_map[parameter]]

            output_grounded_predicates.add(GroundedPredicate(name=predicate_name,
                                                             signature=predicate_signature,
                                                             object_mapping=predicate_object_binding))
        return output_grounded_predicates

    def ground(self):
        """

        :return:
        """
        # First matching the lifted action signature to the grounded objects.
        parameters_map = {lifted_param: grounded_object
                          for lifted_param, grounded_object in zip(self.action.signature, self.grounded_call_objects)}

        self.grounded_positive_preconditions = self.ground_predicates(self.action.positive_preconditions, parameters_map)
        self.grounded_negative_preconditions = self.ground_predicates(self.action.negative_preconditions, parameters_map)
        self.grounded_add_effects = self.ground_predicates(self.action.add_effects, parameters_map)
        self.grounded_delete_effects = self.ground_predicates(self.action.delete_effects, parameters_map)



    def is_applicable(self, state: State) -> bool:
        """"""
