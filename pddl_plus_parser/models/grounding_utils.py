"""Nodule that contains utilities for grounding PDDL+ actions."""
from typing import Dict, List, Set

from anytree import AnyNode

from pddl_plus_parser.models.numerical_expression import NumericalExpressionTree
from pddl_plus_parser.models.pddl_action import Action
from pddl_plus_parser.models.pddl_domain import Domain
from pddl_plus_parser.models.pddl_function import PDDLFunction
from pddl_plus_parser.models.pddl_predicate import (
    SignatureType,
    GroundedPredicate,
    Predicate,
)


def _iterate_calc_tree_and_ground(
    calc_node: AnyNode, parameters_map: Dict[str, str], domain: Domain
) -> AnyNode:
    """Recursion function that iterates over the lifted calculation tree and grounds its elements.

    :param calc_node: the current node the recursion currently visits.
    :param parameters_map: the mapping between the action parameters and the objects in which the action was called.
    :return: the node that represents the calculations of the current lifted expression.
    """
    if calc_node.is_leaf:
        if isinstance(calc_node.value, PDDLFunction):
            lifted_function: PDDLFunction = calc_node.value
            lifted_function_params = [param for param in lifted_function.signature]
            grounded_signature = {}
            for index, parameter_name in enumerate(lifted_function_params):
                if parameter_name in domain.constants:
                    grounded_signature[parameter_name] = lifted_function.signature[
                        parameter_name
                    ]

                else:
                    grounded_signature[
                        parameters_map[lifted_function_params[index]]
                    ] = lifted_function.signature[parameter_name]

            grounded_function = PDDLFunction(
                name=lifted_function.name, signature=grounded_signature
            )
            return AnyNode(id=str(grounded_function), value=grounded_function)

        return AnyNode(id=calc_node.id, value=calc_node.value)

    return AnyNode(
        id=calc_node.id,
        value=calc_node.value,
        children=[
            _iterate_calc_tree_and_ground(
                calc_node.children[0], parameters_map, domain
            ),
            _iterate_calc_tree_and_ground(
                calc_node.children[1], parameters_map, domain
            ),
        ],
    )


def ground_numeric_calculation_tree(
    lifted_numeric_exp_tree: NumericalExpressionTree,
    parameters_map: Dict[str, str],
    domain: Domain,
) -> NumericalExpressionTree:
    """grounds a calculation expression and returns the version containing the objects instead of the parameters.

    :param lifted_numeric_exp_tree: the lifted calculation tree.
    :param parameters_map: the mapping between the action's parameters and the objects in which the action
        was called with.
    :param domain: the domain in which the action was called.
    :return: the grounded expression tree.
    """
    root = lifted_numeric_exp_tree.root
    grounded_root = _iterate_calc_tree_and_ground(root, parameters_map, domain)
    return NumericalExpressionTree(expression_tree=grounded_root)


def fix_grounded_predicate_types(
    lifted_predicate_params: List[str],
    predicate_signature: SignatureType,
    domain: Domain,
    action: Action,
) -> None:
    """Fix the types of the grounded predicate to match those in the action itself.

    :param lifted_predicate_params: the names of the lifted predicate parameters.
    :param predicate_signature: the signature of the grounded predicate.
    """
    for domain_def_parameter, lifted_predicate_param_name in zip(
        predicate_signature, lifted_predicate_params
    ):
        if lifted_predicate_param_name in domain.constants:
            predicate_signature[domain_def_parameter] = domain.constants[
                lifted_predicate_param_name
            ].type

        else:
            predicate_signature[domain_def_parameter] = action.signature[
                lifted_predicate_param_name
            ]


def ground_predicate(
    predicate: Predicate, parameters_map: Dict[str, str], domain: Domain, action: Action
) -> GroundedPredicate:
    """Ground a predicate.

    :param predicate: the predicate to ground.
    :param parameters_map: the mapping of parameters to objects.
    :return: the grounded predicate.
    """
    predicate_name = predicate.name
    # I want the grounded predicate to have the same signature as the original signature so that I can later
    # on efficiently search for it in the states.
    predicate_signature = {
        param: param_type
        for param, param_type in domain.predicates[predicate_name].signature.items()
    }
    predicate_params = list(predicate.signature.keys())
    if len(domain.constants) > 0:
        predicate_params.extend(list(domain.constants.keys()))

    lifted_predicate_params = [param for param in predicate.signature]
    predicate_object_mapping = {}
    for index, parameter_name in enumerate(predicate_signature):
        if predicate_params[index] in domain.constants:
            predicate_object_mapping[parameter_name] = predicate_params[index]

        else:
            predicate_object_mapping[parameter_name] = parameters_map[
                predicate_params[index]
            ]

    # Matching the types to be the same as the ones in the action.
    fix_grounded_predicate_types(
        lifted_predicate_params, predicate_signature, domain, action
    )

    return GroundedPredicate(
        name=predicate_name,
        signature=predicate_signature,
        object_mapping=predicate_object_mapping,
        is_positive=predicate.is_positive,
    )


def ground_numeric_expressions(
    lifted_numeric_exp_tree: Set[NumericalExpressionTree],
    parameters_map: Dict[str, str],
    domain: Domain,
) -> Set[NumericalExpressionTree]:
    """Grounds a set of numeric expressions.

    :param lifted_numeric_exp_tree: the set containing the numeric expressions to ground.
    :param parameters_map: the mapping between the action's parameters and the objects using which the action was
        called.
    :return: a set containing the grounded expressions.
    """
    grounded_numeric_expressions = set()
    for expression in lifted_numeric_exp_tree:
        grounded_numeric_expressions.add(
            ground_numeric_calculation_tree(expression, parameters_map, domain)
        )

    return grounded_numeric_expressions
