from anytree import RenderTree, PreOrderIter, AnyNode

from pddl_plus_parser.models import construct_expression_tree, PDDLFunction, PDDLType, calculate, evaluate_expression

SIMPLE_EXPRESSION = ['assign', ['amount', '?jug1'], '0']
COMPLEX_EXPRESSION = ['>=', ['-', ['capacity', '?jug2'], ['amount', '?jug2']], ['amount', '?jug1']]

TEST_DOMAIN_FUNCTIONS = {
    "capacity": PDDLFunction(name="capacity", signature={"?jug": PDDLType(name="jug")}),
    "amount": PDDLFunction(name="amount", signature={"?jug": PDDLType(name="jug")})
}


def test_construct_expression_tree_constructs_simple_expression_correctly():
    node_tree = construct_expression_tree(SIMPLE_EXPRESSION, TEST_DOMAIN_FUNCTIONS)
    print(RenderTree(node_tree))

    expected_node_ids = ["assign", "(amount ?jug1 - jug)", "0.0"]
    for index, node in enumerate(PreOrderIter(node_tree)):
        assert node.id == expected_node_ids[index]


def test_construct_expression_tree_constructs_complex_expression_correctly():
    node_tree = construct_expression_tree(COMPLEX_EXPRESSION, TEST_DOMAIN_FUNCTIONS)
    print(RenderTree(node_tree))

    expected_node_ids = [">=", "-", "(capacity ?jug2 - jug)", "(amount ?jug2 - jug)", "(amount ?jug1 - jug)"]
    for index, node in enumerate(PreOrderIter(node_tree)):
        assert node.id == expected_node_ids[index]


def test_calculate_returns_correct_calculation_on_simple_tree():
    root = AnyNode(id="root", value="*", children=[
        AnyNode(id="sub0", value=12),
        AnyNode(id="sub1", value=5)
    ])
    assert calculate(root) == 60.0


def test_calculate_returns_correct_calculation_on_a_more_complex_tree():
    root = AnyNode(id="root", value="*", children=[
        AnyNode(id="d1", value="+", children=[
            AnyNode(id="sub0", value=2),
            AnyNode(id="sub1", value=5)
        ]),
        AnyNode(id="d2", value="-", children=[
            AnyNode(id="d3", value="/", children=[
                AnyNode(id="sub0", value=100),
                AnyNode(id="sub1", value=4)
            ]),
            AnyNode(id="sub4", value=5)
        ])
    ])
    assert calculate(root) == 140.0

def test_evaluate_expression_evaluates_simple_pddl_ast():
    test_expression = ['>=', ['amount', '?jug1'], '-3.5']
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    print(RenderTree(root))

    result = evaluate_expression(root)
    assert result == True

def test_evaluate_expression_evaluates_another_simple_pddl_ast():
    test_expression = ['>=', ['amount', '?jug1'], '3.5']
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    print(RenderTree(root))

    result = evaluate_expression(root)
    assert result == False


def test_evaluate_expression_evaluates_complex_pddl_ast():
    test_expression = ['>=', ['/', ['+', ['amount', '?jug1'], '12'], ['+', ['amount', '?jug2'], '4']], '4.5']
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    print(RenderTree(root))

    result = evaluate_expression(root)
    assert result == False