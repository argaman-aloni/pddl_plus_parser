"""module to represent an operator that can apply actions and change state objects."""
from typing import List, Set, Dict, NoReturn

from anytree import AnyNode

from . import PDDLFunction
from .numerical_expression import NumericalExpressionTree, evaluate_expression
from .pddl_action import Action
from .pddl_domain import Domain
from .pddl_predicate import GroundedPredicate, Predicate
from .pddl_state import State


def set_expression_value(expression_node: AnyNode, state_fluents: Dict[str, PDDLFunction]) -> NoReturn:
    """Set the value of the expression according to the fluents present in the state.

    :param expression_node: the node that is currently being observed.
    """
    if expression_node.is_leaf:
        if not isinstance(expression_node.value, PDDLFunction):
            return

        grounded_fluent: PDDLFunction = expression_node.value
        grounded_fluent.set_value(state_fluents[str(grounded_fluent)].value)
        return

    set_expression_value(expression_node.children[0], state_fluents)
    set_expression_value(expression_node.children[1], state_fluents)


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
        """Grounds predicates that appear in the grounded operator.

        :param lifted_predicates: the lifted predicates definition originating from the domain.
        :param parameters_map: the mapping between the action's parameters and the objects that the action
            was actually called with.
        :return: the predicates that appear in the action containing concrete objects.
        """
        output_grounded_predicates = set()
        for predicate in lifted_predicates:
            predicate_name = predicate.name
            # I want the grounded predicate to have the same signature as the original signature so that I can later
            # on efficiently search for it in the states.
            predicate_signature = {param: param_type for param, param_type in
                                   self.domain.predicates[predicate_name].signature.items()}
            lifted_predicate_params = [param for param in predicate.signature]
            predicate_object_mapping = {
                parameter_name: parameters_map[lifted_predicate_params[index]] for index, parameter_name in
                enumerate(predicate_signature)}

            # Matching the types to be the same as the ones in the action.
            for domain_def_parameter, lifted_predicate_param_name in zip(predicate_signature, lifted_predicate_params):
                predicate_signature[domain_def_parameter] = self.action.signature[lifted_predicate_param_name]

            output_grounded_predicates.add(GroundedPredicate(name=predicate_name,
                                                             signature=predicate_signature,
                                                             object_mapping=predicate_object_mapping))
        return output_grounded_predicates

    def iterate_calc_tree_and_ground(self, calc_node: AnyNode, parameters_map: Dict[str, str]) -> AnyNode:
        """Recursion function that iterates over the lifted calculation tree and grounds its elements.

        :param calc_tree: the current node the recursion currently visits.
        :param parameters_map: the mapping between the action parameters and the objects in which the action was called.
        :return: the node that represents the calculations of the current lifted expression.
        """
        if calc_node.is_leaf:
            if isinstance(calc_node.value, PDDLFunction):
                lifted_function: PDDLFunction = calc_node.value
                lifted_function_params = [param for param in lifted_function.signature]
                grounded_signature = {
                    parameters_map[lifted_function_params[index]]: lifted_function.signature[parameter_name] for
                    index, parameter_name in enumerate(lifted_function_params)}
                grounded_function = PDDLFunction(name=lifted_function.name,
                                                 signature=grounded_signature)
                return AnyNode(id=str(grounded_function), value=grounded_function)

            return AnyNode(id=calc_node.id, value=calc_node.value)

        return AnyNode(
            id=calc_node.id, value=calc_node.value, children=[
                self.iterate_calc_tree_and_ground(calc_node.children[0], parameters_map),
                self.iterate_calc_tree_and_ground(calc_node.children[1], parameters_map),
            ])

    def ground_numeric_calculation_tree(self, lifted_numeric_exp_tree: NumericalExpressionTree,
                                        parameters_map: Dict[str, str]) -> NumericalExpressionTree:
        """grounds a calculation expression and returns the version containing the objects instead of the parameters.

        :param lifted_numeric_exp_tree: the lifted calculation tree.
        :param parameters_map: the mapping between the action's parameters and the objects in which the action
            was called with.
        :return: the grounded expression tree.
        """
        root = lifted_numeric_exp_tree.root
        grounded_root = self.iterate_calc_tree_and_ground(root, parameters_map)
        return NumericalExpressionTree(expression_tree=grounded_root)

    def ground_numeric_expressions(self, lifted_numeric_exp_tree: Set[NumericalExpressionTree],
                                   parameters_map: Dict[str, str]) -> Set[NumericalExpressionTree]:
        """Grounds a set of numeric expressions.

        :param lifted_numeric_exp_tree: the set containing the numeric expressions to ground.
        :param parameters_map: the mapping between the action's parameters and the objects using which the action was
            called.
        :return: a set containing the grounded expressions.
        """
        grounded_numeric_expressions = set()
        for expression in lifted_numeric_exp_tree:
            grounded_numeric_expressions.add(self.ground_numeric_calculation_tree(expression, parameters_map))

        return grounded_numeric_expressions

    def ground(self) -> NoReturn:
        """grounds the operator's preconditions and effects."""
        # First matching the lifted action signature to the grounded objects.
        parameters_map = {lifted_param: grounded_object
                          for lifted_param, grounded_object in zip(self.action.signature, self.grounded_call_objects)}

        self.grounded_positive_preconditions = self.ground_predicates(self.action.positive_preconditions,
                                                                      parameters_map)
        self.grounded_negative_preconditions = self.ground_predicates(self.action.negative_preconditions,
                                                                      parameters_map)
        self.grounded_add_effects = self.ground_predicates(self.action.add_effects, parameters_map)
        self.grounded_delete_effects = self.ground_predicates(self.action.delete_effects, parameters_map)

        self.grounded_numeric_preconditions = self.ground_numeric_expressions(self.action.numeric_preconditions,
                                                                              parameters_map)
        self.grounded_numeric_effects = self.ground_numeric_expressions(self.action.numeric_effects, parameters_map)

    def is_applicable(self, state: State) -> bool:
        """Checks if the action is applicable on the current state.

        :param state: the state prior to the action's execution.
        :return: whether or not the action is applicable.
        """
        # Checking that the boolean preconditions hold.
        for positive_precondition in self.grounded_positive_preconditions:
            try:
                state_grounded_predicates = state.state_predicates[str(positive_precondition)]
                if not positive_precondition in state_grounded_predicates:
                    return False

            except KeyError:
                return False

        # Checking that the negative preconditions do not exist in the state predicates.
        for negative_precondition in self.grounded_negative_preconditions:
            try:
                state_grounded_predicates = state.state_predicates[str(negative_precondition)]
                if negative_precondition in state_grounded_predicates:
                    return False

            except KeyError:
                continue

        # Checking that the value of the numeric expression holds.
        for grounded_expression in self.grounded_numeric_preconditions:
            try:
                set_expression_value(grounded_expression.root, state.state_fluents)
                if not evaluate_expression(grounded_expression.root):
                    return False

            except KeyError:
                return False

        return True

