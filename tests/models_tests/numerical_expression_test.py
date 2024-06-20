import pytest
from anytree import RenderTree, PreOrderIter, AnyNode

from pddl_plus_parser.lisp_parsers import PDDLTokenizer, DomainParser
from pddl_plus_parser.models import construct_expression_tree, PDDLFunction, PDDLType, calculate, evaluate_expression, \
    NumericalExpressionTree
from pddl_plus_parser.models.numerical_expression import COMPARISON_OPERATORS
from tests.models_tests.consts import ZENO_DOMAIN_PATH

SIMPLE_EXPRESSION = ['assign', ['amount', '?jug1'], '0']
COMPLEX_EXPRESSION = ['>=', ['-', ['capacity', '?jug2'], ['amount', '?jug2']], ['amount', '?jug1']]

TEST_DOMAIN_FUNCTIONS = {
    "capacity": PDDLFunction(name="capacity", signature={"?jug": PDDLType(name="jug")}),
    "amount": PDDLFunction(name="amount", signature={"?jug": PDDLType(name="jug")})
}


def test_equality_with_epsilon_returns_true_when_numbers_are_smaller_than_epsilon():
    """Test that the function returns true when the numbers are smaller to epsilon."""
    assert COMPARISON_OPERATORS["="](0.00000001, 0.00000002)


def test_equality_with_epsilon_returns_true_when_numbers_are_equal_to_epsilon():
    """Test that the function returns true when the numbers are equal to epsilon."""
    assert COMPARISON_OPERATORS["="](0.0001, 0.0002)


def test_equality_with_epsilon_returns_false_when_numbers_are_larger_to_epsilon():
    """Test that the function returns true when the numbers are close to epsilon."""
    assert not COMPARISON_OPERATORS["="](0.0001, 0.0003)


def test_inequality_with_epsilon_returns_false_when_numbers_are_smaller_than_epsilon():
    """Test that the function returns true when the numbers are smaller to epsilon."""
    assert not COMPARISON_OPERATORS["!="](0.00000001, 0.00000002)


def test_inequality_with_epsilon_returns_false_when_numbers_are_equal_to_epsilon():
    """Test that the function returns true when the numbers are equal to epsilon."""
    assert not COMPARISON_OPERATORS["!="](0.0001, 0.0002)


def test_inequality_with_epsilon_returns_true_when_numbers_are_larger_to_epsilon():
    """Test that the function returns true when the numbers are close to epsilon."""
    assert COMPARISON_OPERATORS["!="](0.0001, 0.0003)


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
    tree = NumericalExpressionTree(root)
    print(tree.to_pddl())

    result = evaluate_expression(root)
    assert result == False


def test_convert_to_pddl_returns_correct_expression():
    test_expression = ['>=', ['capacity', '?jug2'], ['amount', '?jug2']]
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    tree = NumericalExpressionTree(root)
    pddl_str = tree.to_pddl()
    assert pddl_str == "(>= (capacity ?jug2) (amount ?jug2))"


def test_to_pddl_does_not_break_effects_format():
    original_expression = "(assign (fuel ?z) (* (capacity ?z) 9.00))"
    expression_tokenizer = PDDLTokenizer(pddl_str=original_expression)
    tokens = expression_tokenizer.parse()
    zeno_domain = DomainParser(domain_path=ZENO_DOMAIN_PATH).parse_domain()
    root = construct_expression_tree(tokens, zeno_domain.functions)
    tree = NumericalExpressionTree(root)
    assert tree.to_pddl() == "(assign (fuel ?z) (* (capacity ?z) 9))"


def test_convert_to_mathematical_returns_correct_expression():
    test_expression = ['>=', ['capacity', '?jug2'], ['amount', '?jug2']]
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    tree = NumericalExpressionTree(root)
    pddl_str = tree.to_mathematical()
    assert pddl_str == "((capacity ?jug2) >= (amount ?jug2))"


def test_iter_on_numerical_expression_tree_returns_correct_node():
    test_expression = ['>=', ['capacity', '?jug2'], ['amount', '?jug2']]
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    tree = NumericalExpressionTree(root)
    nodes = [node for node in tree]
    assert len(nodes) == 3
    assert nodes[0].id == ">="
    assert nodes[1].id == "(capacity ?jug2 - jug)"
    assert nodes[2].id == "(amount ?jug2 - jug)"


def test_iter_on_numerical_expression_tree_returns_correct_node_on_complex_tree():
    test_expression = ['>=', ['/', ['+', ['amount', '?jug1'], '12'], ['+', ['amount', '?jug2'], '4']], '4.5']
    root = construct_expression_tree(test_expression, TEST_DOMAIN_FUNCTIONS)
    tree = NumericalExpressionTree(root)
    nodes = [node for node in tree]
    assert len(nodes) == 9


def test_simplify_complex_numerical_pddl_expression_returns_inequality_with_correct_fields_and_smaller_length():
    original_expression = "(<= (+ (* (+ (* (- (fuel ?a) 8823.0) -0.01) (+ (* (- (capacity ?a) 8823.0) -0.01) (+ (* (total-fuel-used ) -0.01) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.19) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.24) (+ (* (* (fuel ?a) (onboard ?a)) 0.05) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) -0.6) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.12) (+ (* (- (* (distance ?c1 ?c2) (slow-burn ?a)) 3136.0) -0.02) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) -0.02) (+ (* (* (distance ?c1 ?c2) (total-fuel-used )) -0.01) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) -0.05) (+ (* (- (* (distance ?c2 ?c1) (slow-burn ?a)) 3136.0) -0.02) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) -0.02) (+ (* (* (distance ?c2 ?c1) (total-fuel-used )) -0.01) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) -0.05) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.19) (+ (* (* (slow-burn ?a) (total-fuel-used )) -0.03) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.24) (+ (* (* (fast-burn ?a) (total-fuel-used )) 0.15) (+ (* (* (capacity ?a) (onboard ?a)) 0.05) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) -0.6) (+ (* (* (total-fuel-used ) (onboard ?a)) -0.03) (* (* (total-fuel-used ) (zoom-limit ?a)) -0.23)))))))))))))))))))))))) -0.35) (+ (* (+ (* (- (fuel ?a) 8823.0) -0.06) (+ (* (- (capacity ?a) 8823.0) -0.06) (+ (* (total-fuel-used ) -0.05) (+ (* (- (* (fuel ?a) (distance ?c1 ?c2)) 6917232.0) -0.01) (+ (* (- (* (fuel ?a) (distance ?c2 ?c1)) 6917232.0) -0.01) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.01) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.37) (+ (* (* (fuel ?a) (onboard ?a)) 0.14) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) 0.13) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.11) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) -0.02) (+ (* (- (* (distance ?c1 ?c2) (capacity ?a)) 6917232.0) -0.01) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) 0.01) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.09) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) -0.02) (+ (* (- (* (distance ?c2 ?c1) (capacity ?a)) 6917232.0) -0.01) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) 0.01) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.09) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.01) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.06) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.37) (+ (* (* (fast-burn ?a) (total-fuel-used )) -0.69) (+ (* (* (capacity ?a) (onboard ?a)) 0.14) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) 0.13) (+ (* (* (total-fuel-used ) (onboard ?a)) 0.22) (* (* (total-fuel-used ) (zoom-limit ?a)) -0.3)))))))))))))))))))))))))) 0.68) (+ (* (+ (* (- (fuel ?a) 8823.0) -0.01) (+ (* (- (capacity ?a) 8823.0) -0.01) (+ (* (total-fuel-used ) 0.02) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.19) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.12) (+ (* (* (fuel ?a) (onboard ?a)) 0.43) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) 0.05) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.11) (+ (* (- (* (distance ?c1 ?c2) (slow-burn ?a)) 3136.0) -0.01) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) 0.05) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.04) (+ (* (- (* (distance ?c2 ?c1) (slow-burn ?a)) 3136.0) -0.01) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) 0.05) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.04) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.19) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.05) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.12) (+ (* (* (fast-burn ?a) (total-fuel-used )) 0.21) (+ (* (* (capacity ?a) (onboard ?a)) 0.43) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) 0.05) (+ (* (* (total-fuel-used ) (onboard ?a)) 0.33) (* (* (total-fuel-used ) (zoom-limit ?a)) 0.59)))))))))))))))))))))))) 0.08) (+ (* (+ (* (- (fuel ?a) 8823.0) -0.07) (+ (* (- (capacity ?a) 8823.0) -0.07) (+ (* (total-fuel-used ) -0.05) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) 0.13) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) 0.08) (+ (* (* (fuel ?a) (onboard ?a)) -0.31) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) -0.15) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.07) (+ (* (- (* (distance ?c1 ?c2) (slow-burn ?a)) 3136.0) 0.01) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) 0.04) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) -0.03) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.14) (+ (* (- (* (distance ?c2 ?c1) (slow-burn ?a)) 3136.0) 0.01) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) 0.04) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) -0.03) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.14) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) 0.13) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.05) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) 0.08) (+ (* (* (capacity ?a) (onboard ?a)) -0.31) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) -0.15) (+ (* (* (total-fuel-used ) (onboard ?a)) 0.8) (* (* (total-fuel-used ) (zoom-limit ?a)) 0.12))))))))))))))))))))))) 0.06) (* (+ (* (- (fuel ?a) 8823.0) -0.11) (+ (* (- (capacity ?a) 8823.0) -0.11) (+ (* (total-fuel-used ) -0.23) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.13) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.4) (+ (* (* (fuel ?a) (onboard ?a)) -0.31) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) 0.17) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) -0.06) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) -0.06) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.23) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) -0.06) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.23) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.13) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.19) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.4) (+ (* (* (fast-burn ?a) (total-fuel-used )) 0.35) (+ (* (* (capacity ?a) (onboard ?a)) -0.31) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) 0.17) (+ (* (* (total-fuel-used ) (onboard ?a)) -0.2) (* (* (total-fuel-used ) (zoom-limit ?a)) 0.14)))))))))))))))))))))) 0.63))))) 0.0)"
    expression_tokenizer = PDDLTokenizer(pddl_str=original_expression)
    tokens = expression_tokenizer.parse()
    zeno_domain = DomainParser(domain_path=ZENO_DOMAIN_PATH).parse_domain()
    root = construct_expression_tree(tokens, zeno_domain.functions)
    tree = NumericalExpressionTree(root)
    simplified_expression = tree.simplify_complex_numerical_pddl_expression()
    assert len(simplified_expression) < len(original_expression)
    try:
        expression_tokenizer = PDDLTokenizer(pddl_str=simplified_expression)
        tokens = expression_tokenizer.parse()
        zeno_domain = DomainParser(domain_path=ZENO_DOMAIN_PATH).parse_domain()
        root = construct_expression_tree(tokens, zeno_domain.functions)
        NumericalExpressionTree(root)

    except Exception:
        pytest.fail()


def test_simplify_complex_numerical_pddl_expression_does_not_break_already_simple_expression():
    original_expression = "(<= (+ (* -1 (fuel ?a)) (* -0.0700 (capacity ?a))) -202.66)"
    expression_tokenizer = PDDLTokenizer(pddl_str=original_expression)
    tokens = expression_tokenizer.parse()
    zeno_domain = DomainParser(domain_path=ZENO_DOMAIN_PATH).parse_domain()
    root = construct_expression_tree(tokens, zeno_domain.functions)
    tree = NumericalExpressionTree(root)
    simplified_expression = tree.simplify_complex_numerical_pddl_expression()
    assert simplified_expression == "(<= (+ (* -1 (fuel ?a)) (* -0.07 (capacity ?a))) -202.66)"
