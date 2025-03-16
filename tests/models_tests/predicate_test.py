"""Tests some basic functionality of the Predicate class."""
from pddl_plus_parser.models import Predicate, PDDLType


def test_predicate_copy_with_negated_option_false_returns_the_previous_predicate_with_its_own_is_positive_value():
    # Arrange
    predicate = Predicate(name="predicate", signature={"param1": PDDLType("object")}, is_positive=True)

    # Act
    result = predicate.copy(is_negated=False)

    # Assert
    assert result.is_positive == predicate.is_positive


def test_predicate_copy_with_negated_option_true_returns_the_previous_predicate_with_is_positive_value_negated_from_original():
    # Arrange
    predicate = Predicate(name="predicate", signature={"param1": PDDLType("object")}, is_positive=True)

    # Act
    result = predicate.copy(is_negated=True)

    # Assert
    assert result.is_positive != predicate.is_positive


def test_predicate_returns_not_equal_when_the_order_in_the_signature_order_is_incorrect():
    # Arrange
    predicate1 = Predicate(name="predicate", signature={"param1": PDDLType("object"),
                                                        "param2": PDDLType("object")}, is_positive=True)
    predicate2 = Predicate(name="predicate", signature={"param2": PDDLType("object"),
                                                        "param1": PDDLType("object")}, is_positive=True)
    # Act
    assert not predicate1 == predicate2


def test_predicate_returns_equal_when_the_order_in_the_signature_order_is_correct():
    # Arrange
    predicate1 = Predicate(name="predicate", signature={"param1": PDDLType("object"),
                                                        "param2": PDDLType("object")}, is_positive=True)
    predicate2 = Predicate(name="predicate", signature={"param1": PDDLType("object"),
                                                        "param2": PDDLType("object")}, is_positive=True)
    # Act
    assert predicate1 == predicate2


def test_predicate_returns_equal_when_the_order_in_the_signature_order_is_correct_and_types_are_subtypes():
    # Arrange
    type1 = PDDLType("object")
    type2 = PDDLType("subtype", parent=type1)
    predicate1 = Predicate(name="predicate", signature={"param1": type2,
                                                        "param2": type2}, is_positive=True)
    predicate2 = Predicate(name="predicate", signature={"param1": type1,
                                                        "param2": type1}, is_positive=True)
    # Act
    assert predicate1 == predicate2


def test_predicate_returns_not_equal_when_the_order_in_the_signature_parameter_is_incorrect():
    # Arrange
    predicate1 = Predicate(name="predicate", signature={"param2": PDDLType("object"),
                                                        "param3": PDDLType("object")}, is_positive=True)
    predicate2 = Predicate(name="predicate", signature={"param2": PDDLType("object"),
                                                        "param1": PDDLType("object")}, is_positive=True)
    # Act
    assert not predicate1 == predicate2


def test_change_signature_returns_correct_form_of_predicate_with_signature_changed():
    # Arrange
    predicate = Predicate(name="predicate", signature={"?x": PDDLType("object"),
                                                       "?y": PDDLType("object")}, is_positive=True)
    expected_predicate_output = Predicate(name="predicate", signature={"?param_0": PDDLType("object"),
                                                                       "?param_1": PDDLType("object")},
                                          is_positive=True)
    predicate.change_signature({
        "?x": "?param_0",
        "?y": "?param_1"
    })
    assert predicate == expected_predicate_output
