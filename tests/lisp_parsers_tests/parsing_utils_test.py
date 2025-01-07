from pddl_plus_parser.lisp_parsers.parsing_utils import parse_predicate_from_string
from pddl_plus_parser.models import ObjectType

def test_from_string_with_predicate_string_returns_predicate_object():
    # Arrange
    predicate_str = "(predicate_name ?param1 - type1 ?param2 - type2)"
    types_map = {"type1": ObjectType, "type2": ObjectType}

    # Act
    result = parse_predicate_from_string(predicate_str, types_map)

    # Assert
    assert result.name == "predicate_name"
    assert result.signature == {"?param1": ObjectType, "?param2": ObjectType}
    print(result.untyped_representation)