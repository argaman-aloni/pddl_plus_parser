"""Module test for the PDDLFunction class."""

from pddl_plus_parser.models import PDDLFunction, PDDLType

OBJECT_TYPE = PDDLType(name="object")
CITY_TYPE = PDDLType(name="city", parent=OBJECT_TYPE)


def test_state_representation_returns_correct_string_when_function_is_lifted():
    """Test that the state representation returns the correct string."""
    fluent = PDDLFunction(
        name="distance", signature={"?c1": CITY_TYPE, "?c2": CITY_TYPE}
    )
    assert fluent.state_representation == "(= (distance ?c1 ?c2) 0)"


def test_state_representation_returns_correct_string_when_function_is_grounded_with_different_variables():
    """Test that the state representation returns the correct string."""
    fluent = PDDLFunction(
        name="distance", signature={"city0": CITY_TYPE, "city1": CITY_TYPE}
    )
    assert fluent.state_representation == "(= (distance city0 city1) 0)"


def test_state_representation_returns_correct_string_when_function_is_grounded_with_the_same_variables():
    """Test that the state representation returns the correct string."""
    fluent = PDDLFunction(
        name="distance",
        signature={"city0": CITY_TYPE},
        repeating_variables={"city0": 2},
    )
    assert fluent.state_representation == "(= (distance city0 city0) 0)"


def test_state_typed_representation_returns_correct_string_when_function_is_grounded_with_the_same_variables():
    """Test that the state representation returns the correct string."""
    fluent = PDDLFunction(
        name="distance",
        signature={"city0": CITY_TYPE},
        repeating_variables={"city0": 2},
    )
    assert (
        fluent.state_typed_representation
        == "(= (distance city0 - city city0 - city) 0)"
    )


def test_change_signature_returns_correct_form_of_function_with_signature_changed():
    # Arrange
    func = PDDLFunction(
        name="function", signature={"?x": PDDLType("object"), "?y": PDDLType("object")}
    )
    expected_function_output = PDDLFunction(
        name="function",
        signature={"?param_0": PDDLType("object"), "?param_1": PDDLType("object")},
    )
    func.change_signature({"?x": "?param_0", "?y": "?param_1"})
    assert func == expected_function_output
