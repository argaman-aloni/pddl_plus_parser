from pddl_plus_parser.models.numeric_symbolic_operations import simplify_complex_numeric_expression, \
    simplify_inequality, simplify_equality


def test_simplify_complex_numeric_expression_with_simple_expression_returns_the_same_expression_in_pddl_format():
    test_simple_expression = "((distance ?c2 ?c1) * (zoom-limit ?a))"
    expected_simple_expression = "(* (distance ?c2 ?c1) (zoom-limit ?a))"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_complex_numeric_expression_with_complex_expression_returns_shorter_version_of_the_original():
    original_pddl_expression = "(+ (* (+ (* (- (fuel ?a) 8823.0) -0.01) (+ (* (- (capacity ?a) 8823.0) -0.01) (+ (* (total-fuel-used ) -0.01) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.19) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.24) (+ (* (* (fuel ?a) (onboard ?a)) 0.05) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) -0.6) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.12) (+ (* (- (* (distance ?c1 ?c2) (slow-burn ?a)) 3136.0) -0.02) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) -0.02) (+ (* (* (distance ?c1 ?c2) (total-fuel-used )) -0.01) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) -0.05) (+ (* (- (* (distance ?c2 ?c1) (slow-burn ?a)) 3136.0) -0.02) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) -0.02) (+ (* (* (distance ?c2 ?c1) (total-fuel-used )) -0.01) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) -0.05) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.19) (+ (* (* (slow-burn ?a) (total-fuel-used )) -0.03) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.24) (+ (* (* (fast-burn ?a) (total-fuel-used )) 0.15) (+ (* (* (capacity ?a) (onboard ?a)) 0.05) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) -0.6) (+ (* (* (total-fuel-used ) (onboard ?a)) -0.03) (* (* (total-fuel-used ) (zoom-limit ?a)) -0.23)))))))))))))))))))))))) -0.35) (+ (* (+ (* (- (fuel ?a) 8823.0) -0.06) (+ (* (- (capacity ?a) 8823.0) -0.06) (+ (* (total-fuel-used ) -0.05) (+ (* (- (* (fuel ?a) (distance ?c1 ?c2)) 6917232.0) -0.01) (+ (* (- (* (fuel ?a) (distance ?c2 ?c1)) 6917232.0) -0.01) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.01) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.37) (+ (* (* (fuel ?a) (onboard ?a)) 0.14) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) 0.13) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.11) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) -0.02) (+ (* (- (* (distance ?c1 ?c2) (capacity ?a)) 6917232.0) -0.01) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) 0.01) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.09) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) -0.02) (+ (* (- (* (distance ?c2 ?c1) (capacity ?a)) 6917232.0) -0.01) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) 0.01) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.09) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.01) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.06) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.37) (+ (* (* (fast-burn ?a) (total-fuel-used )) -0.69) (+ (* (* (capacity ?a) (onboard ?a)) 0.14) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) 0.13) (+ (* (* (total-fuel-used ) (onboard ?a)) 0.22) (* (* (total-fuel-used ) (zoom-limit ?a)) -0.3)))))))))))))))))))))))))) 0.68) (+ (* (+ (* (- (fuel ?a) 8823.0) -0.01) (+ (* (- (capacity ?a) 8823.0) -0.01) (+ (* (total-fuel-used ) 0.02) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.19) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.12) (+ (* (* (fuel ?a) (onboard ?a)) 0.43) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) 0.05) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.11) (+ (* (- (* (distance ?c1 ?c2) (slow-burn ?a)) 3136.0) -0.01) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) 0.05) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.04) (+ (* (- (* (distance ?c2 ?c1) (slow-burn ?a)) 3136.0) -0.01) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) 0.05) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.04) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.19) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.05) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.12) (+ (* (* (fast-burn ?a) (total-fuel-used )) 0.21) (+ (* (* (capacity ?a) (onboard ?a)) 0.43) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) 0.05) (+ (* (* (total-fuel-used ) (onboard ?a)) 0.33) (* (* (total-fuel-used ) (zoom-limit ?a)) 0.59)))))))))))))))))))))))) 0.08) (+ (* (+ (* (- (fuel ?a) 8823.0) -0.07) (+ (* (- (capacity ?a) 8823.0) -0.07) (+ (* (total-fuel-used ) -0.05) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) 0.13) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) 0.08) (+ (* (* (fuel ?a) (onboard ?a)) -0.31) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) -0.15) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) 0.07) (+ (* (- (* (distance ?c1 ?c2) (slow-burn ?a)) 3136.0) 0.01) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) 0.04) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) -0.03) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.14) (+ (* (- (* (distance ?c2 ?c1) (slow-burn ?a)) 3136.0) 0.01) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) 0.04) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) -0.03) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.14) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) 0.13) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.05) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) 0.08) (+ (* (* (capacity ?a) (onboard ?a)) -0.31) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) -0.15) (+ (* (* (total-fuel-used ) (onboard ?a)) 0.8) (* (* (total-fuel-used ) (zoom-limit ?a)) 0.12))))))))))))))))))))))) 0.06) (* (+ (* (- (fuel ?a) 8823.0) -0.11) (+ (* (- (capacity ?a) 8823.0) -0.11) (+ (* (total-fuel-used ) -0.23) (+ (* (- (* (fuel ?a) (slow-burn ?a)) 35292.0) -0.13) (+ (* (- (* (fuel ?a) (fast-burn ?a)) 97053.0) -0.4) (+ (* (* (fuel ?a) (onboard ?a)) -0.31) (+ (* (- (* (fuel ?a) (zoom-limit ?a)) 44115.0) 0.17) (+ (* (- (* (distance ?c1 ?c2) (distance ?c2 ?c1)) 614656.0) -0.06) (+ (* (- (* (distance ?c1 ?c2) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c1 ?c2) (onboard ?a)) -0.06) (+ (* (- (* (distance ?c1 ?c2) (zoom-limit ?a)) 3920.0) 0.23) (+ (* (- (* (distance ?c2 ?c1) (fast-burn ?a)) 8624.0) 0.01) (+ (* (* (distance ?c2 ?c1) (onboard ?a)) -0.06) (+ (* (- (* (distance ?c2 ?c1) (zoom-limit ?a)) 3920.0) 0.23) (+ (* (- (* (slow-burn ?a) (capacity ?a)) 35292.0) -0.13) (+ (* (* (slow-burn ?a) (total-fuel-used )) 0.19) (+ (* (- (* (fast-burn ?a) (capacity ?a)) 97053.0) -0.4) (+ (* (* (fast-burn ?a) (total-fuel-used )) 0.35) (+ (* (* (capacity ?a) (onboard ?a)) -0.31) (+ (* (- (* (capacity ?a) (zoom-limit ?a)) 44115.0) 0.17) (+ (* (* (total-fuel-used ) (onboard ?a)) -0.2) (* (* (total-fuel-used ) (zoom-limit ?a)) 0.14)))))))))))))))))))))) 0.63)))))"
    test_complex_expression = "((((((fuel ?a) - 8823.0) * -0.01) + ((((capacity ?a) - 8823.0) * -0.01) + (((total-fuel-used ) * -0.01) + (((((fuel ?a) * (slow-burn ?a)) - 35292.0) * -0.19) + (((((fuel ?a) * (fast-burn ?a)) - 97053.0) * -0.24) + ((((fuel ?a) * (onboard ?a)) * 0.05) + (((((fuel ?a) * (zoom-limit ?a)) - 44115.0) * -0.6) + (((((distance ?c1 ?c2) * (distance ?c2 ?c1)) - 614656.0) * 0.12) + (((((distance ?c1 ?c2) * (slow-burn ?a)) - 3136.0) * -0.02) + (((((distance ?c1 ?c2) * (fast-burn ?a)) - 8624.0) * -0.02) + ((((distance ?c1 ?c2) * (total-fuel-used )) * -0.01) + (((((distance ?c1 ?c2) * (zoom-limit ?a)) - 3920.0) * -0.05) + (((((distance ?c2 ?c1) * (slow-burn ?a)) - 3136.0) * -0.02) + (((((distance ?c2 ?c1) * (fast-burn ?a)) - 8624.0) * -0.02) + ((((distance ?c2 ?c1) * (total-fuel-used )) * -0.01) + (((((distance ?c2 ?c1) * (zoom-limit ?a)) - 3920.0) * -0.05) + (((((slow-burn ?a) * (capacity ?a)) - 35292.0) * -0.19) + ((((slow-burn ?a) * (total-fuel-used )) * -0.03) + (((((fast-burn ?a) * (capacity ?a)) - 97053.0) * -0.24) + ((((fast-burn ?a) * (total-fuel-used )) * 0.15) + ((((capacity ?a) * (onboard ?a)) * 0.05) + (((((capacity ?a) * (zoom-limit ?a)) - 44115.0) * -0.6) + ((((total-fuel-used ) * (onboard ?a)) * -0.03) + (((total-fuel-used ) * (zoom-limit ?a)) * -0.23)))))))))))))))))))))))) * -0.35) + ((((((fuel ?a) - 8823.0) * -0.06) + ((((capacity ?a) - 8823.0) * -0.06) + (((total-fuel-used ) * -0.05) + (((((fuel ?a) * (distance ?c1 ?c2)) - 6917232.0) * -0.01) + (((((fuel ?a) * (distance ?c2 ?c1)) - 6917232.0) * -0.01) + (((((fuel ?a) * (slow-burn ?a)) - 35292.0) * -0.01) + (((((fuel ?a) * (fast-burn ?a)) - 97053.0) * -0.37) + ((((fuel ?a) * (onboard ?a)) * 0.14) + (((((fuel ?a) * (zoom-limit ?a)) - 44115.0) * 0.13) + (((((distance ?c1 ?c2) * (distance ?c2 ?c1)) - 614656.0) * 0.11) + (((((distance ?c1 ?c2) * (fast-burn ?a)) - 8624.0) * -0.02) + (((((distance ?c1 ?c2) * (capacity ?a)) - 6917232.0) * -0.01) + ((((distance ?c1 ?c2) * (onboard ?a)) * 0.01) + (((((distance ?c1 ?c2) * (zoom-limit ?a)) - 3920.0) * 0.09) + (((((distance ?c2 ?c1) * (fast-burn ?a)) - 8624.0) * -0.02) + (((((distance ?c2 ?c1) * (capacity ?a)) - 6917232.0) * -0.01) + ((((distance ?c2 ?c1) * (onboard ?a)) * 0.01) + (((((distance ?c2 ?c1) * (zoom-limit ?a)) - 3920.0) * 0.09) + (((((slow-burn ?a) * (capacity ?a)) - 35292.0) * -0.01) + ((((slow-burn ?a) * (total-fuel-used )) * 0.06) + (((((fast-burn ?a) * (capacity ?a)) - 97053.0) * -0.37) + ((((fast-burn ?a) * (total-fuel-used )) * -0.69) + ((((capacity ?a) * (onboard ?a)) * 0.14) + (((((capacity ?a) * (zoom-limit ?a)) - 44115.0) * 0.13) + ((((total-fuel-used ) * (onboard ?a)) * 0.22) + (((total-fuel-used ) * (zoom-limit ?a)) * -0.3)))))))))))))))))))))))))) * 0.68) + ((((((fuel ?a) - 8823.0) * -0.01) + ((((capacity ?a) - 8823.0) * -0.01) + (((total-fuel-used ) * 0.02) + (((((fuel ?a) * (slow-burn ?a)) - 35292.0) * -0.19) + (((((fuel ?a) * (fast-burn ?a)) - 97053.0) * -0.12) + ((((fuel ?a) * (onboard ?a)) * 0.43) + (((((fuel ?a) * (zoom-limit ?a)) - 44115.0) * 0.05) + (((((distance ?c1 ?c2) * (distance ?c2 ?c1)) - 614656.0) * 0.11) + (((((distance ?c1 ?c2) * (slow-burn ?a)) - 3136.0) * -0.01) + (((((distance ?c1 ?c2) * (fast-burn ?a)) - 8624.0) * 0.01) + ((((distance ?c1 ?c2) * (onboard ?a)) * 0.05) + (((((distance ?c1 ?c2) * (zoom-limit ?a)) - 3920.0) * 0.04) + (((((distance ?c2 ?c1) * (slow-burn ?a)) - 3136.0) * -0.01) + (((((distance ?c2 ?c1) * (fast-burn ?a)) - 8624.0) * 0.01) + ((((distance ?c2 ?c1) * (onboard ?a)) * 0.05) + (((((distance ?c2 ?c1) * (zoom-limit ?a)) - 3920.0) * 0.04) + (((((slow-burn ?a) * (capacity ?a)) - 35292.0) * -0.19) + ((((slow-burn ?a) * (total-fuel-used )) * 0.05) + (((((fast-burn ?a) * (capacity ?a)) - 97053.0) * -0.12) + ((((fast-burn ?a) * (total-fuel-used )) * 0.21) + ((((capacity ?a) * (onboard ?a)) * 0.43) + (((((capacity ?a) * (zoom-limit ?a)) - 44115.0) * 0.05) + ((((total-fuel-used ) * (onboard ?a)) * 0.33) + (((total-fuel-used ) * (zoom-limit ?a)) * 0.59)))))))))))))))))))))))) * 0.08) + ((((((fuel ?a) - 8823.0) * -0.07) + ((((capacity ?a) - 8823.0) * -0.07) + (((total-fuel-used ) * -0.05) + (((((fuel ?a) * (slow-burn ?a)) - 35292.0) * 0.13) + (((((fuel ?a) * (fast-burn ?a)) - 97053.0) * 0.08) + ((((fuel ?a) * (onboard ?a)) * -0.31) + (((((fuel ?a) * (zoom-limit ?a)) - 44115.0) * -0.15) + (((((distance ?c1 ?c2) * (distance ?c2 ?c1)) - 614656.0) * 0.07) + (((((distance ?c1 ?c2) * (slow-burn ?a)) - 3136.0) * 0.01) + (((((distance ?c1 ?c2) * (fast-burn ?a)) - 8624.0) * 0.04) + ((((distance ?c1 ?c2) * (onboard ?a)) * -0.03) + (((((distance ?c1 ?c2) * (zoom-limit ?a)) - 3920.0) * 0.14) + (((((distance ?c2 ?c1) * (slow-burn ?a)) - 3136.0) * 0.01) + (((((distance ?c2 ?c1) * (fast-burn ?a)) - 8624.0) * 0.04) + ((((distance ?c2 ?c1) * (onboard ?a)) * -0.03) + (((((distance ?c2 ?c1) * (zoom-limit ?a)) - 3920.0) * 0.14) + (((((slow-burn ?a) * (capacity ?a)) - 35292.0) * 0.13) + ((((slow-burn ?a) * (total-fuel-used )) * 0.05) + (((((fast-burn ?a) * (capacity ?a)) - 97053.0) * 0.08) + ((((capacity ?a) * (onboard ?a)) * -0.31) + (((((capacity ?a) * (zoom-limit ?a)) - 44115.0) * -0.15) + ((((total-fuel-used ) * (onboard ?a)) * 0.8) + (((total-fuel-used ) * (zoom-limit ?a)) * 0.12))))))))))))))))))))))) * 0.06) + (((((fuel ?a) - 8823.0) * -0.11) + ((((capacity ?a) - 8823.0) * -0.11) + (((total-fuel-used ) * -0.23) + (((((fuel ?a) * (slow-burn ?a)) - 35292.0) * -0.13) + (((((fuel ?a) * (fast-burn ?a)) - 97053.0) * -0.4) + ((((fuel ?a) * (onboard ?a)) * -0.31) + (((((fuel ?a) * (zoom-limit ?a)) - 44115.0) * 0.17) + (((((distance ?c1 ?c2) * (distance ?c2 ?c1)) - 614656.0) * -0.06) + (((((distance ?c1 ?c2) * (fast-burn ?a)) - 8624.0) * 0.01) + ((((distance ?c1 ?c2) * (onboard ?a)) * -0.06) + (((((distance ?c1 ?c2) * (zoom-limit ?a)) - 3920.0) * 0.23) + (((((distance ?c2 ?c1) * (fast-burn ?a)) - 8624.0) * 0.01) + ((((distance ?c2 ?c1) * (onboard ?a)) * -0.06) + (((((distance ?c2 ?c1) * (zoom-limit ?a)) - 3920.0) * 0.23) + (((((slow-burn ?a) * (capacity ?a)) - 35292.0) * -0.13) + ((((slow-burn ?a) * (total-fuel-used )) * 0.19) + (((((fast-burn ?a) * (capacity ?a)) - 97053.0) * -0.4) + ((((fast-burn ?a) * (total-fuel-used )) * 0.35) + ((((capacity ?a) * (onboard ?a)) * -0.31) + (((((capacity ?a) * (zoom-limit ?a)) - 44115.0) * 0.17) + ((((total-fuel-used ) * (onboard ?a)) * -0.2) + (((total-fuel-used ) * (zoom-limit ?a)) * 0.14)))))))))))))))))))))) * 0.63)))))"
    result = simplify_complex_numeric_expression(test_complex_expression)
    assert len(result) < len(original_pddl_expression)


def test_simplify_removes_zero_multiplications_from_expression_and_reduces_string_length():
    test_simple_expression = "(0.0 * ((distance ?c2 ?c1) * (zoom-limit ?a)))"
    expected_simple_expression = "0"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_removes_multiplication_by_one_sice_it_does_not_change_the_expression():
    test_simple_expression = "(1.0 * ((distance ?c2 ?c1) * (zoom-limit ?a)))"
    expected_simple_expression = "(* (* (zoom-limit ?a) (distance ?c2 ?c1)) 1)"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_when_there_is_a_multiplication_causing_the_creation_of_power_does_not_add_power_symbol():
    test_simple_expression = "(1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1)))"
    expected_simple_expression = "(* (* (distance ?c2 ?c1) (distance ?c2 ?c1)) 1)"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_when_there_is_a_multiplication_causing_the_creation_of_power_does_not_add_power_symbol_with_complex_expression():
    test_simple_expression = "((((capacity ?a) - 8823.0) * -0.01) + (1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1) * (distance ?c2 ?c1))))"
    expected_simple_expression = "(+ (+ (* (capacity ?a) -0.01) (* (* (* (distance ?c2 ?c1) (distance ?c2 ?c1)) (distance ?c2 ?c1)) 1)) 88.23)"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_when_there_are_zeros_in_the_original_expression_removes_them_from_the_output():
    test_simple_expression = "((((capacity ?a) - 8823.0) * 0) + (1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1) * (distance ?c2 ?c1))))"
    expected_simple_expression = "(* (* (* (distance ?c2 ?c1) (distance ?c2 ?c1)) (distance ?c2 ?c1)) 1)"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_when_there_are_zeros_in_the_expression_with_decimal_point_removes_zeros_correctly():
    # expression = (+ (*(load_limit ?x) 0.00)(+ (*(current_load ?x) 0.01)(*(fuel - cost) - 1.00))
    test_simple_expression = "((((distance ?c2 ?c1) * 0.00) + ((zoom-limit ?a) * 0.01)) + ((capacity ?a) * -1.00))"
    expected_simple_expression = "(+ (* (zoom-limit ?a) 0.01) (* (capacity ?a) -1))"
    result = simplify_complex_numeric_expression(test_simple_expression)
    assert result == expected_simple_expression


def test_simplify_inequality_when_given_simple_inequality_returns_the_same_inequality():
    test_simple_inequality = "((distance ?c2 ?c1) <= (zoom-limit ?a))"
    expected_simple_inequality = "(<= (distance ?c2 ?c1) (zoom-limit ?a))"
    result = simplify_inequality(test_simple_inequality)
    assert result == expected_simple_inequality


def test_simplify_inequality_when_given_a_truth_expression_returns_none():
    test_simple_inequality = "((distance ?c2 ?c1) <= (distance ?c2 ?c1))"
    result = simplify_inequality(test_simple_inequality)
    assert result is None


def test_simplify_inequality_when_given_a_number_returns_the_number():
    test_simple_inequality = "0"
    result = simplify_inequality(test_simple_inequality)
    assert result == "0"


def test_simplify_inequality_when_given_complex_expression_with_no_assumptions_returns_simplified_version():
    original_expression = "(((((capacity ?a) - 8823.0) * 1.5) + (1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1) * (distance ?c2 ?c1)))) <= 3657.14)"
    result = simplify_inequality(original_expression)
    assert len(result) < len(original_expression)
    assert result.endswith("0)")


def test_simplify_inequality_when_given_complex_expression_with_assumptions_on_linear_dependency_removes_the_assumptions_from_the_original_expression():
    original_expression = "(((((capacity ?a) - 8823.0) * 1.5) + (1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1) * (distance ?c2 ?c1)))) <= 3657.14)"
    assumption = ["(capacity ?a) = (-1 * ((distance ?c2 ?c1) * -1))"]
    result = simplify_inequality(original_expression, assumption)
    assert len(result) < len(original_expression)
    assert "(capacity ?a)" not in result


def test_simplify_inequality_when_given_complex_expression_with_assumptions_on_linear_dependency_removes_assumption_even_when_assumption_in_complex_form():
    original_expression = "(((((capacity ?a) - 8823.0) * 1.5) + (1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1) * (distance ?c2 ?c1)))) <= 3657.14)"
    assumption = ["((capacity ?a) - 54) = (-1 * (((distance ?c2 ?c1) - 54) * -1))"]
    result = simplify_inequality(original_expression, assumption)
    assert len(result) < len(original_expression)
    assert "(capacity ?a)" not in result


def test_simplify_inequality_when_rhs_is_zero_does_not_add_invalid_none_at_the_end_of_the_expression():
    original_expression = "(((((capacity ?a) - 1.0) * 1.5) + (1.0 * ((distance ?c2 ?c1) * (distance ?c2 ?c1) * (distance ?c2 ?c1)))) <= 0)"
    assumption = ["((capacity ?a) - 54) = (-1 * (((distance ?c2 ?c1) - 54) * -1))"]
    result = simplify_inequality(original_expression, assumption)
    assert "None" not in result


def test_simplify_equality_when_given_an_equality_without_assumptions_returns_correct_equality():
    original_expression = "((capacity ?a) - 54) = (-1 * (((distance ?c2 ?c1) - 54) * -1))"
    assumption = []
    result = simplify_equality(original_expression, assumption)
    assert len(result) < len(original_expression)
    assert result == "(= (capacity ?a) (distance ?c2 ?c1))"


def test_simplify_equality_when_given_an_equality_that_is_trivial_returns_none():
    original_expression = "((capacity ?a) - 54) = ((capacity ?a) - 54)"
    assumption = []
    result = simplify_equality(original_expression, assumption)
    assert result is None
