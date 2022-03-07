from pytest import fixture, raises

from lisp_parsers import DomainParser, PDDLTokenizer
from models import PDDLType, Predicate
from tests.lisp_parsers_tests.consts import TEST_PARSING_FILE_PATH, TEST_WOODWORKING_DOMAIN_PATH, \
    TEST_NUMERIC_DEPOT_DOMAIN_PATH

test_types_with_no_parent = ['acolour', 'awood', 'woodobj', 'machine', 'surface', 'treatmentstatus', 'aboardsize',
                             'apartsize']

nested_types = ['acolour', 'awood', 'woodobj', 'machine', 'surface', 'treatmentstatus', 'aboardsize', 'apartsize',
                '-', 'object', 'highspeed-saw', 'saw', 'glazer', 'grinder', 'immersion-varnisher', 'planer',
                'spray-varnisher', '-', 'machine', 'board', 'part', '-', 'woodobj']

test_constants = ['small', 'medium', 'large', '-', 'apartsize', 'highspeed-saw', 'varnished', 'glazed', 'untreated',
                  'colourfragments', '-', 'treatmentstatus',
                  'natural', '-', 'acolour', 'verysmooth', 'smooth', 'rough', '-', 'surface']

test_predicates_str = """((available ?obj - woodobj)
	(surface-condition ?obj - woodobj ?surface - surface)
	(treatment ?obj - part ?treatment - treatmentstatus)
	(colour ?obj - part ?colour - acolour)
	(wood ?obj - woodobj ?wood - awood)
	(is-smooth ?surface - surface)
	(has-colour ?agent - machine ?colour - acolour)
	(goalsize ?part - part ?size - apartsize)
	(boardsize-successor ?size1 - aboardsize ?size2 - aboardsize)
	(unused ?obj - part)
	(boardsize ?board - board ?size - aboardsize)
	(empty ?agent - highspeed-saw)
	(in-highspeed-saw ?b - board ?agent - highspeed-saw)
	(grind-treatment-change ?agent - grinder ?old - treatmentstatus ?new - treatmentstatus))"""


@fixture()
def domain_parser() -> DomainParser:
    return DomainParser(TEST_PARSING_FILE_PATH)


def test_parse_types_with_no_parent_extracts_types_with_object_as_parent(domain_parser: DomainParser):
    parsed_types = domain_parser.parse_types(test_types_with_no_parent)
    assert len(parsed_types) == len(test_types_with_no_parent) + 1
    for type_name, expected_type_name in zip(parsed_types.keys(), test_types_with_no_parent):
        assert type_name == expected_type_name
        assert parsed_types[type_name].parent.name == "object"


def test_parse_types_with_object_parent_not_create_duplicates(domain_parser: DomainParser):
    test_types_with_object_parent = ['acolour', 'awood', 'woodobj', 'machine', 'surface', 'treatmentstatus',
                                     'aboardsize', 'apartsize', '-', 'object']

    parsed_types = domain_parser.parse_types(test_types_with_object_parent)
    assert len(parsed_types) == len(test_types_with_no_parent) + 1
    for type_name, expected_type_name in zip(parsed_types.keys(), test_types_with_no_parent):
        assert type_name == expected_type_name
        assert parsed_types[type_name].parent.name == "object"


def test_parse_types_with_deep_type_hierarchy_recognizes_ancestors_correctly(domain_parser: DomainParser):
    test_types_deep_hierarchy = ['place', 'locatable', '-', 'object', 'hoist', 'surface',
                                 '-', 'locatable', 'pallet', '-', 'surface']

    parsed_types = domain_parser.parse_types(test_types_deep_hierarchy)
    assert "pallet" in parsed_types
    assert parsed_types["pallet"].parent.name == "surface"
    assert parsed_types["pallet"].parent.parent.name == "locatable"
    assert parsed_types["pallet"].parent.parent.parent.name == "object"


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
    for const in constants.values():
        assert const.name in valid_constants


def test_parse_constants_with_nexted_constants_extract_correct_constants_data(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    domain_consts = domain_parser.parse_constants(test_constants, domain_types)

    assert list(domain_consts.keys()) == ['small', 'medium', 'large', 'highspeed-saw', 'varnished', 'glazed',
                                          'untreated', 'colourfragments', 'natural', 'verysmooth', 'smooth', 'rough']


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


def test_parse_predicate_with_no_parameters_returns_predicate_object_with_only_name_and_empty_signature(
        domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    test_predicate_no_params_ast = ["ok"]
    predicate = domain_parser.parse_predicate(test_predicate_no_params_ast, domain_types)
    assert predicate is not None
    assert predicate.name == "ok"
    assert len(predicate.signature) == 0


def test_parse_predicates_with_single_predicate_returns_predicates_dictionary_correctly(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    test_predicates = [['available', '?obj', '-', 'woodobj']]
    predicates = domain_parser.parse_predicates(test_predicates, domain_types)
    assert "available" in predicates


def test_parse_predicates_with_multiple_predicate_returns_predicates_dictionary_correctly(domain_parser: DomainParser):
    tokenizer = PDDLTokenizer(pddl_str=test_predicates_str)
    domain_types = domain_parser.parse_types(nested_types)
    predicates = domain_parser.parse_predicates(tokenizer.parse(), domain_types)
    assert len(predicates) == 14


def test_parse_functions_with_single_function_extract_function_data_correctly(domain_parser: DomainParser):
    test_pddl_function = "((velocity ?saw - highspeed-saw))"
    tokenizer = PDDLTokenizer(pddl_str=test_pddl_function)
    domain_types = domain_parser.parse_types(nested_types)
    functions = domain_parser.parse_functions(tokenizer.parse(), domain_types)
    assert len(functions) == 1
    assert "velocity" in functions
    assert str(functions["velocity"]) == "(velocity ?saw - highspeed-saw)"


def test_parse_functions_with_multiple_functions_extract_functions_correctly(domain_parser: DomainParser):
    test_pddl_functions = "((velocity ?saw - highspeed-saw)" \
                          "(distance-to-floor ?m - machine))"
    tokenizer = PDDLTokenizer(pddl_str=test_pddl_functions)
    domain_types = domain_parser.parse_types(nested_types)
    functions = domain_parser.parse_functions(tokenizer.parse(), domain_types)
    assert len(functions) == 2


def test_parse_function_with_no_parameters_returns_function_object_with_only_name_and_empty_signature(
        domain_parser: DomainParser):
    test_function_no_params = "((total-cost))"
    tokenizer = PDDLTokenizer(pddl_str=test_function_no_params)
    domain_types = domain_parser.parse_types(nested_types)
    functions = domain_parser.parse_functions(tokenizer.parse(), domain_types)
    assert functions is not None
    assert len(functions) == 1
    assert "total-cost" in functions


def test_parse_action_with_boolean_action_type_returns_action_data_correctly(domain_parser: DomainParser):
    test_action_str = """(do-spray-varnish
	:parameters   (?m - spray-varnisher ?x - part ?newcolour - acolour ?surface - surface)
	:precondition (and (available ?x) (has-colour ?m ?newcolour) (surface-condition ?x ?surface) (is-smooth ?surface) (treatment ?x untreated))
	:effect       (and (treatment ?x varnished) (colour ?x ?newcolour) (not (treatment ?x untreated)) (not (colour ?x natural))))"""
    action_tokens = PDDLTokenizer(pddl_str=test_action_str).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=test_predicates_str).parse()
    domain_types = domain_parser.parse_types(nested_types)
    domain_consts = domain_parser.parse_constants(test_constants, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    action = domain_parser.parse_action(action_tokens, domain_types, domain_functions, domain_predicates, domain_consts)

    assert action.name == "do-spray-varnish"
    assert action.signature == {
        "?m": PDDLType("spray-varnisher"),
        "?x": PDDLType("part"),
        "?newcolour": PDDLType("acolour"),
        "?surface": PDDLType("surface"),
    }
    assert action.negative_preconditions == set()
    expected_preconditions = {
        Predicate(name="available", signature={"?x": PDDLType("part")}),
        Predicate(name="has-colour", signature={
            "?m": PDDLType("spray-varnisher"),
            "?newcolour": PDDLType("acolour")
        }),
        Predicate(name="surface-condition", signature={
            "?x": PDDLType("part"),
            "?surface": PDDLType("surface")
        }),
        Predicate(name="is-smooth", signature={
            "?surface": PDDLType("surface")
        }),
        Predicate(name="treatment", signature={
            "?x": PDDLType("part"),
            "untreated": PDDLType("treatmentstatus")
        }),

    }
    assert len(action.positive_preconditions) == len(expected_preconditions)
    for precondition in expected_preconditions:
        assert precondition in action.positive_preconditions

    expected_add_effects = {
        Predicate(name="colour", signature={
            "?x": PDDLType("part"),
            "?newcolour": PDDLType("acolour")
        }),
        Predicate(name="treatment", signature={
            "?x": PDDLType("part"),
            "varnished": PDDLType("treatmentstatus")
        })
    }
    assert len(action.add_effects) == len(expected_add_effects)
    for effect in expected_add_effects:
        assert effect in action.add_effects

    expected_delete_effects = {
        Predicate(name="treatment", signature={
            "?x": PDDLType("part"),
            "untreated": PDDLType("treatmentstatus")
        }),
        Predicate(name="colour", signature={
            "?x": PDDLType("part"),
            "natural": PDDLType("acolour")
        })
    }

    assert len(action.add_effects) == len(expected_delete_effects)
    for effect in expected_delete_effects:
        assert effect in action.delete_effects


def test_parse_simple_action_with_numeric_preconditions_and_effects_extracts_the_calculation_tree_correctly(
        domain_parser: DomainParser):
    test_simple_types = """(place locatable - object
	    depot distributor - place
        truck hoist surface - locatable
        pallet crate - surface)"""
    test_simple_predicates = """((at ?x - locatable ?y - place) 
             (on ?x - crate ?y - surface)
             (in ?x - crate ?y - truck)
             (lifting ?x - hoist ?y - crate)
             (available ?x - hoist)
             (clear ?x - surface))"""
    test_domain_simple_functions = """((load_limit ?t - truck) 
	(current_load ?t - truck) 
	(weight ?c - crate)
	(fuel-cost))
    """
    test_simple_numeric_action = """(Load
        :parameters (?x - hoist ?y - crate ?z - truck ?p - place)
        :precondition (and (at ?x ?p) (at ?z ?p) (lifting ?x ?y)
                (<= (+ (current_load ?z) (weight ?y)) (load_limit ?z)))
        :effect (and (not (lifting ?x ?y)) (in ?y ?z) (available ?x)
                (increase (current_load ?z) (weight ?x))))"""
    types_tokens = PDDLTokenizer(pddl_str=test_simple_types).parse()
    functions_tokens = PDDLTokenizer(pddl_str=test_domain_simple_functions).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=test_simple_predicates).parse()
    action_tokens = PDDLTokenizer(pddl_str=test_simple_numeric_action).parse()

    domain_types = domain_parser.parse_types(types_tokens)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = domain_parser.parse_functions(functions_tokens, domain_types)

    action = domain_parser.parse_action(action_tokens, domain_types, domain_functions, domain_predicates)
    assert len(action.numeric_preconditions) == 1
    precond_expression = action.numeric_preconditions.pop()
    assert precond_expression.root.id == "<="
    assert precond_expression.root.height == 2

    assert len(action.numeric_effects) == 1
    effect_expression = action.numeric_effects.pop()
    assert effect_expression.root.id == "increase"
    assert effect_expression.root.height == 1


def test_parse_simple_domain_with_only_boolean_actions_succeeds_in_parsing_all_domain_parts(
        domain_parser: DomainParser):
    domain = domain_parser.parse_domain()
    assert domain is not None
    assert len(domain.requirements) == 2
    assert len(domain.types) == 8
    assert len(domain.predicates) == 3
    assert len(domain.actions) == 6


def test_parse_woodworking_domain_with_boolean_actions_and_constants_succeeds_in_parsing_all_domain_parts():
    domain_parser = DomainParser(TEST_WOODWORKING_DOMAIN_PATH)
    domain = domain_parser.parse_domain()
    assert domain is not None
    assert len(domain.requirements) == 2
    assert len(domain.types) == 18
    assert len(domain.constants) == 11
    assert len(domain.predicates) == 14
    assert len(domain.actions) == 13


def test_parse_depot_domain_with_numric_actions_succeeds_in_parsing_all_domain_parts():
    domain_parser = DomainParser(TEST_NUMERIC_DEPOT_DOMAIN_PATH)
    domain = domain_parser.parse_domain()
    assert domain is not None
    assert len(domain.requirements) == 2
    assert len(domain.types) == 10
    assert len(domain.predicates) == 6
    assert len(domain.functions) == 4
    assert len(domain.actions) == 5
