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
