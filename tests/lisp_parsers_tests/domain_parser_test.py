from pytest import fixture, raises

from lisp_parsers import DomainParser
from tests.lisp_parsers_tests.consts import TEST_PARSING_FILE_PATH

test_types_with_no_parent = ['acolour', 'awood', 'woodobj', 'machine', 'surface', 'treatmentstatus', 'aboardsize',
                             'apartsize']

nested_types = ['acolour', 'awood', 'woodobj', 'machine', 'surface', 'treatmentstatus', 'aboardsize', 'apartsize',
                '-', 'object', 'highspeed-saw', 'saw', 'glazer', 'grinder', 'immersion-varnisher', 'planer',
                'spray-varnisher', '-', 'machine', 'board', 'part', '-', 'woodobj']


@fixture()
def domain_parser() -> DomainParser:
    return DomainParser(TEST_PARSING_FILE_PATH)


def test_parse_types_with_no_parent_extracts_types_with_object_as_parent(domain_parser: DomainParser):
    parsed_types = domain_parser.parse_types(test_types_with_no_parent)
    assert len(parsed_types) == len(test_types_with_no_parent)
    for type_name, expected_type_name in zip(parsed_types.keys(), test_types_with_no_parent):
        assert type_name == expected_type_name
        assert parsed_types[type_name].parent.name == "object"


def test_parse_types_with_object_parent_not_create_duplicates(domain_parser: DomainParser):
    test_types_with_object_parent = ['acolour', 'awood', 'woodobj', 'machine', 'surface', 'treatmentstatus',
                                     'aboardsize', 'apartsize', '-', 'object']

    parsed_types = domain_parser.parse_types(test_types_with_object_parent)
    assert len(parsed_types) == len(test_types_with_no_parent)
    for type_name, expected_type_name in zip(parsed_types.keys(), test_types_with_no_parent):
        assert type_name == expected_type_name
        assert parsed_types[type_name].parent.name == "object"


def test_parse_types_with_type_hierarchy_recognize_nested_types(domain_parser: DomainParser):
    parsed_types = domain_parser.parse_types(nested_types)
    for object_descendant in test_types_with_no_parent:
        assert parsed_types[object_descendant].parent.name == "object"

    machine_types = ['highspeed-saw', 'saw', 'glazer', 'grinder', 'immersion-varnisher', 'planer', 'spray-varnisher']
    for machine_descendant in machine_types:
        assert parsed_types[machine_descendant].parent.name == "machine"

    wood_object_types = ['board', 'part']
    for wood_obj_descendant in wood_object_types:
        assert parsed_types[wood_obj_descendant].parent.name == "woodobj"

    assert parsed_types["machine"].parent.name == "object"
    assert parsed_types["woodobj"].parent.name == "object"


def test_parse_constants_when_given_invalid_type_raises_syntax_error(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    with raises(SyntaxError):
        bad_constants = ['small', 'medium', 'large', '-', 'bad-type']
        domain_parser.parse_constants(bad_constants, domain_types)

def test_parse_constants_when_given_valid_type_extract_constants(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    valid_constants = ['small', 'medium', 'large', '-', 'apartsize']
    constants = domain_parser.parse_constants(valid_constants, domain_types)
    assert len(constants) == 3
    for const in constants:
        assert const.name in valid_constants

def test_parse_predicate_with_legal_predicate_data_is_successful(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    test_predicate = ['available', '?obj', '-', 'woodobj']
    predicate = domain_parser.parse_predicate(test_predicate, domain_types)
    assert predicate.name == "available"
    assert "?obj" in predicate.signature

def test_parse_predicate_with_illegal_predicate_data_raises_error(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    with raises(SyntaxError):
        test_predicate = ['available', '?obj', 'woodobj']
        domain_parser.parse_predicate(test_predicate, domain_types)

def test_