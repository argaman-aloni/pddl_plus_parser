from pytest import fixture, raises, fail

from pddl_plus_parser.lisp_parsers import DomainParser, PDDLTokenizer
from pddl_plus_parser.models import PDDLType, Predicate, Action, CompoundPrecondition
from tests.lisp_parsers_tests.consts import TEST_PARSING_FILE_PATH, TEST_WOODWORKING_DOMAIN_PATH, \
    TEST_NUMERIC_DEPOT_DOMAIN_PATH, PLANT_WATERING_DOMAIN, TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN, \
    TEST_TYPES_FOR_CONDITIONAL_DOMAIN, TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN, SPIDER_DOMAIN_PATH, \
    TYPES_FOR_UNIVERSAL_CONDITIONAL_DOMAIN, TEST_PREDICATES_FOR_UNIVERSAL_QUANTIFIER_DOMAIN, UMT2_DOMAIN_PATH, \
    MICONIC_LEARNED_DOMAIN_PATH

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
    predicate = domain_parser._parse_predicate(test_predicate, domain_types)
    assert predicate.name == "available"
    assert "?obj" in predicate.signature


def test_parse_predicate_with_illegal_predicate_data_raises_error(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    with raises(SyntaxError):
        test_predicate = ['available', '?obj', 'woodobj']
        domain_parser._parse_predicate(test_predicate, domain_types)


def test_parse_predicate_with_no_parameters_returns_predicate_object_with_only_name_and_empty_signature(
        domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    test_predicate_no_params_ast = ["ok"]
    predicate = domain_parser._parse_predicate(test_predicate_no_params_ast, domain_types)
    assert predicate is not None
    assert predicate.name == "ok"
    assert len(predicate.signature) == 0


def test_parse_predicates_with_single_predicate_returns_predicates_dictionary_correctly(domain_parser: DomainParser):
    domain_types = domain_parser.parse_types(nested_types)
    test_predicates = [['available', '?obj', '-', 'woodobj']]
    predicates = domain_parser.parse_predicates(test_predicates, domain_types)
    assert "available" in predicates


def test_parse_predicates_with_private_predicates_extracts_predicates_correctly(domain_parser: DomainParser):
    private_predicates_str = """((:private
	(surface-condition ?obj - woodobj ?surface - surface)
	(treatment ?obj - part ?treatment - treatmentstatus)
    ))"""

    tokenizer = PDDLTokenizer(pddl_str=private_predicates_str)
    domain_types = domain_parser.parse_types(nested_types)
    predicates = domain_parser.parse_predicates(tokenizer.parse(), domain_types)
    assert "surface-condition" in predicates
    assert predicates["surface-condition"].untyped_representation == "(surface-condition ?obj ?surface)"
    assert "treatment" in predicates
    assert predicates["treatment"].untyped_representation == "(treatment ?obj ?treatment)"


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


def test_parse_action_with_inequality_precondition_adds_the_lifted_objects_correctly(domain_parser: DomainParser):
    test_action_str = """(cut-board-medium
	:parameters   (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
	:precondition (and (unused ?p) (not (= ?size_before ?size_after)) (goalsize ?p medium) (in-highspeed-saw ?b ?m) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s1 ?size_before))
	:effect       (and (boardsize ?b ?size_after) (available ?p) (surface-condition ?p ?surface) (treatment ?p untreated) (wood ?p ?w) (colour ?p natural) (not (unused ?p))))"""
    action_tokens = PDDLTokenizer(pddl_str=test_action_str).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=test_predicates_str).parse()
    domain_types = domain_parser.parse_types(nested_types)
    domain_consts = domain_parser.parse_constants(test_constants, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    action = domain_parser.parse_action(action_tokens, domain_types, domain_functions, domain_predicates, domain_consts)

    assert action.name == "cut-board-medium"
    assert action.preconditions.root.inequality_preconditions == {("?size_before", "?size_after")}


def test_parse_action_with_equality_precondition_adds_the_lifted_objects_correctly(domain_parser: DomainParser):
    test_action_str = """(cut-board-medium
	:parameters   (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
	:precondition (and (unused ?p) (= ?size_before ?size_after) (goalsize ?p medium) (in-highspeed-saw ?b ?m) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s1 ?size_before))
	:effect       (and (boardsize ?b ?size_after) (available ?p) (surface-condition ?p ?surface) (treatment ?p untreated) (wood ?p ?w) (colour ?p natural) (not (unused ?p))))"""
    action_tokens = PDDLTokenizer(pddl_str=test_action_str).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=test_predicates_str).parse()
    domain_types = domain_parser.parse_types(nested_types)
    domain_consts = domain_parser.parse_constants(test_constants, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    action = domain_parser.parse_action(action_tokens, domain_types, domain_functions, domain_predicates, domain_consts)

    assert action.name == "cut-board-medium"
    assert action.preconditions.root.equality_preconditions == {("?size_before", "?size_after")}


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
    assert expected_preconditions.issubset(action.preconditions.root.operands)
    assert action.preconditions.root.operands.issubset(expected_preconditions)
    print()
    print(str(action.preconditions))


def test_parse_action_with_conditional_effects_with_one_condition_and_one_effect_parse_correctly(
        domain_parser: DomainParser):
    conditional_effects = """(and (when
            (not (CAN-CONTINUE-GROUP ?c ?to))
            (make-unmovable ?to)
    ))"""
    types_tokens = PDDLTokenizer(pddl_str=TEST_TYPES_FOR_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN).parse()
    constants_tokens = PDDLTokenizer(pddl_str=TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN).parse()
    effects_tokens = PDDLTokenizer(pddl_str=conditional_effects).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_consts = domain_parser.parse_constants(constants_tokens, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    new_action = Action()
    new_action.name = "test-action"
    new_action.signature = {"?c": domain_types["card"], "?from": domain_types["cardposition"],
                            "?fromdeal": domain_types["deal"], "?to": domain_types["card"],
                            "?totableau": domain_types["tableau"]}
    domain_parser.parse_effects(effects_ast=effects_tokens,
                                new_action=new_action,
                                domain_types=domain_types,
                                domain_functions=domain_functions,
                                domain_predicates=domain_predicates,
                                domain_constants=domain_consts)
    conditional_effect = new_action.conditional_effects.pop()
    assert conditional_effect is not None
    print(str(conditional_effect))
    assert str(
        conditional_effect) == "(when (and (not (CAN-CONTINUE-GROUP ?c ?to))) (and (make-unmovable ?to)))".lower()


def test_parse_action_with_conditional_effects_with_one_condition_and_two_effects_parse_correctly(
        domain_parser: DomainParser):
    conditional_effects = """(and (when
            (not (can-continue-group ?c ?to))
            (and
                (currently-updating-unmovable)
                (make-unmovable ?to)
            )
    ))"""
    types_tokens = PDDLTokenizer(pddl_str=TEST_TYPES_FOR_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN).parse()
    constants_tokens = PDDLTokenizer(pddl_str=TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN).parse()
    effects_tokens = PDDLTokenizer(pddl_str=conditional_effects).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_consts = domain_parser.parse_constants(constants_tokens, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    new_action = Action()
    new_action.name = "test-action"
    new_action.signature = {"?c": domain_types["card"], "?from": domain_types["cardposition"],
                            "?fromdeal": domain_types["deal"], "?to": domain_types["card"],
                            "?totableau": domain_types["tableau"]}
    domain_parser.parse_effects(effects_ast=effects_tokens,
                                new_action=new_action,
                                domain_types=domain_types,
                                domain_functions=domain_functions,
                                domain_predicates=domain_predicates,
                                domain_constants=domain_consts)
    conditional_effect = new_action.conditional_effects.pop()
    assert conditional_effect is not None
    negative_condition = str(conditional_effect.antecedents)
    add_effects = conditional_effect.discrete_effects
    assert negative_condition == "(and (not (can-continue-group ?c ?to)))"
    print([eff.untyped_representation for eff in add_effects])
    assert len(add_effects) == 2
    effects_str = {effect.untyped_representation for effect in add_effects}
    assert effects_str == {"(currently-updating-unmovable )", "(make-unmovable ?to)"}


def test_parse_action_with_conditional_effects_with_two_conditions_and_two_effects_parse_correctly(
        domain_parser: DomainParser):
    conditional_effects = """(and (when
            (and (can-continue-group ?c ?to) (not (can-continue-group ?c ?from)))
            (and (currently-updating-unmovable) (make-unmovable ?to))))"""
    types_tokens = PDDLTokenizer(pddl_str=TEST_TYPES_FOR_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN).parse()
    constants_tokens = PDDLTokenizer(pddl_str=TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN).parse()
    effects_tokens = PDDLTokenizer(pddl_str=conditional_effects).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_consts = domain_parser.parse_constants(constants_tokens, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    new_action = Action()
    new_action.name = "test-action"
    new_action.signature = {"?c": domain_types["card"], "?from": domain_types["cardposition"],
                            "?fromdeal": domain_types["deal"], "?to": domain_types["card"],
                            "?totableau": domain_types["tableau"]}
    domain_parser.parse_effects(effects_ast=effects_tokens,
                                new_action=new_action,
                                domain_types=domain_types,
                                domain_functions=domain_functions,
                                domain_predicates=domain_predicates,
                                domain_constants=domain_consts)
    conditional_effect = new_action.conditional_effects.pop()
    assert conditional_effect is not None
    antecedents = str(conditional_effect.antecedents)
    add_effects = conditional_effect.discrete_effects
    assert "(not (can-continue-group ?c ?from))" in antecedents
    assert "(can-continue-group ?c ?to)" in antecedents
    assert len(add_effects) == 2
    effects_str = {effect.untyped_representation for effect in add_effects}
    assert effects_str == {"(currently-updating-unmovable )", "(make-unmovable ?to)"}
    print(conditional_effect)


def test_parse_action_with_conditional_effects_succeeds_in_parsing_action_and_returns_correct_fields(
        domain_parser: DomainParser):
    test_action_with_conditional_effects = """(deal-card
    :parameters (?c - card ?from - cardposition ?fromdeal - deal ?to - card ?totableau - tableau)
    :precondition
    (and
        (currently-dealing)
        (not (currently-updating-movable))
        (not (currently-updating-unmovable))
        (not (currently-updating-part-of-tableau))
        (not (currently-collecting-deck))
        (current-deal ?fromdeal)
        (TO-DEAL ?c ?totableau ?fromdeal ?from)
        (clear ?c)
        (on ?c ?from)
        (part-of-tableau ?to ?totableau)
        (clear ?to)
    )
    :effect
    (and
        (not (on ?c ?from))
        (on ?c ?to)
        (not (clear ?to))
        (clear ?from)
        (in-play ?c)
        (part-of-tableau ?c ?totableau)
        (movable ?c)
        (when
            (not (CAN-CONTINUE-GROUP ?c ?to))
            (and
                (currently-updating-unmovable)
                (make-unmovable ?to)
            )
        )
    )
    )"""
    types_tokens = PDDLTokenizer(pddl_str=TEST_TYPES_FOR_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN).parse()
    constants_tokens = PDDLTokenizer(pddl_str=TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN).parse()
    action_tokens = PDDLTokenizer(pddl_str=test_action_with_conditional_effects).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_consts = domain_parser.parse_constants(constants_tokens, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    action = domain_parser.parse_action(action_tokens, domain_types, domain_functions, domain_predicates, domain_consts)
    assert action is not None
    assert action.name == "deal-card"
    assert action.conditional_effects is not None


def test_parse_action_with_conditional_effect_raises_error_if_conditional_effect_not_in_correct_format(
        domain_parser: DomainParser):
    conditional_effects_str = """(and 
    (when (and (currently-updating-unmovable) (make-unmovable ?to))))"""
    types_tokens = PDDLTokenizer(pddl_str=TEST_TYPES_FOR_CONDITIONAL_DOMAIN).parse()
    constants_tokens = PDDLTokenizer(pddl_str=TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN).parse()
    conditional_effect_tokens = PDDLTokenizer(pddl_str=conditional_effects_str).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_consts = domain_parser.parse_constants(constants_tokens, domain_types)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}  # Functions are irrelevant for this case.
    action = Action()
    action.name = "deal-card"
    action.signature = {"?c": domain_types["card"], "?from": domain_types["cardposition"],
                        "?fromdeal": domain_types["deal"], "?to": domain_types["card"],
                        "?totableau": domain_types["tableau"]}
    with raises(SyntaxError):
        domain_parser.parse_effects(conditional_effect_tokens, action, domain_types, domain_functions,
                                    domain_predicates, domain_consts)


def test_parse_action_with_universal_quantifier_in_preconditions_returns_correct_universal_precondition(
        domain_parser: DomainParser):
    test_action_with_universal_precondition = """
    (stop
      :parameters (?f - floor)
      :precondition (and (forall (?p - passenger) (and (lift-at ?f) (not (boarded ?p)))))
      :effect (and (not (lift-at ?f)))
    ))"""
    types_tokens = PDDLTokenizer(pddl_str=TYPES_FOR_UNIVERSAL_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_UNIVERSAL_QUANTIFIER_DOMAIN).parse()
    action_tokens = PDDLTokenizer(pddl_str=test_action_with_universal_precondition).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}
    action = domain_parser.parse_action(action_ast=action_tokens, domain_types=domain_types,
                                        domain_functions=domain_functions, domain_predicates=domain_predicates)
    assert action is not None
    universal_precondition = action.preconditions.root.operands.pop()
    assert universal_precondition is not None
    assert len(universal_precondition.operands) == 2
    assert universal_precondition.quantified_parameter == "?p"
    assert universal_precondition.quantified_type == domain_types["passenger"]


def test_parse_action_with_both_universal_preconditions_and_regular_ones_creates_correct_preconditions(
        domain_parser: DomainParser):
    test_action_with_universal_precondition = """
    (stop
      :parameters (?f1 - floor ?f2 - floor)
      :precondition (and (above ?f1 ?f2) (forall (?p - passenger) (and (lift-at ?f1) (not (boarded ?p)))))
      :effect (and (not (lift-at ?f1)))
    ))"""
    types_tokens = PDDLTokenizer(pddl_str=TYPES_FOR_UNIVERSAL_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_UNIVERSAL_QUANTIFIER_DOMAIN).parse()
    action_tokens = PDDLTokenizer(pddl_str=test_action_with_universal_precondition).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}
    action = domain_parser.parse_action(action_ast=action_tokens, domain_types=domain_types,
                                        domain_functions=domain_functions, domain_predicates=domain_predicates)
    assert action is not None
    preconditions = action.preconditions.root.operands
    assert preconditions is not None
    assert len(preconditions) == 2
    for op, cond in action.preconditions:
        print(str(cond))


def test_parse_action_with_universal_quantifier_in_conditional_effect_returns_correct_universal_quantifier_data(
        domain_parser: DomainParser):
    test_action_with_universal_quantifier = """
    (stop
      :parameters (?f - floor)
      :precondition (lift-at ?f)
      :effect (and 
                   (forall (?p - passenger) 
                      (when (and (boarded ?p) 
                                 (destin ?p ?f))
                            (and (not (boarded ?p)) 
                                 (served  ?p))))
    ))"""
    types_tokens = PDDLTokenizer(pddl_str=TYPES_FOR_UNIVERSAL_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_UNIVERSAL_QUANTIFIER_DOMAIN).parse()
    action_tokens = PDDLTokenizer(pddl_str=test_action_with_universal_quantifier).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}
    action = domain_parser.parse_action(action_ast=action_tokens, domain_types=domain_types,
                                        domain_functions=domain_functions, domain_predicates=domain_predicates)
    assert action is not None
    universal_effects = action.universal_effects
    assert len(universal_effects) == 1
    universal_effect = universal_effects.pop()
    assert universal_effect.quantified_parameter == "?p"
    assert universal_effect.quantified_type.name == "passenger"
    conditional_effect = universal_effect.conditional_effects.pop()
    assert len(conditional_effect.discrete_effects) == 2
    antecedents = conditional_effect.antecedents.root.operands
    assert len(antecedents) == 2


def test_parse_action_with_two_universal_quantifiers_in_effect_extract_all_universal_effects(
        domain_parser: DomainParser):
    test_action_with_universal_quantifier = """
    (stop
      :parameters (?f - floor)
      :precondition (lift-at ?f)
      :effect (and 
               (forall (?p - passenger) 
                  (when (and (boarded ?p) 
                             (destin ?p ?f))
                        (and (not (boarded ?p)) 
                             (served  ?p))))
               (forall (?p - passenger)                
                   (when (and (origin ?p ?f) (not (served ?p)))
                              (boarded ?p)))))"""
    types_tokens = PDDLTokenizer(pddl_str=TYPES_FOR_UNIVERSAL_CONDITIONAL_DOMAIN).parse()
    predicate_tokens = PDDLTokenizer(pddl_str=TEST_PREDICATES_FOR_UNIVERSAL_QUANTIFIER_DOMAIN).parse()
    action_tokens = PDDLTokenizer(pddl_str=test_action_with_universal_quantifier).parse()
    domain_types = domain_parser.parse_types(types_tokens)
    domain_predicates = domain_parser.parse_predicates(predicate_tokens, domain_types)
    domain_functions = {}
    action = domain_parser.parse_action(action_ast=action_tokens, domain_types=domain_types,
                                        domain_functions=domain_functions, domain_predicates=domain_predicates)
    assert action is not None
    universal_effects = action.universal_effects
    assert len(universal_effects) == 2


def test_parse_simple_action_with_only_numeric_preconditions_and_effects_extracts_the_correct_preconditions_tree(
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
        :precondition (and (<= (+ (current_load ?z) (weight ?y)) (load_limit ?z)))
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
    assert len(action.preconditions.root.operands) == 1
    precond_expression = action.preconditions.root.operands.pop()
    assert precond_expression.root.id == "<="
    assert precond_expression.root.height == 2


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
    assert len(action.preconditions.root.operands) == 4

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


def test_parse_depot_domain_with_numeric_actions_succeeds_in_parsing_all_domain_parts():
    domain_parser = DomainParser(TEST_NUMERIC_DEPOT_DOMAIN_PATH)
    domain = domain_parser.parse_domain()
    assert domain is not None
    assert len(domain.requirements) == 2
    assert len(domain.types) == 10
    assert len(domain.predicates) == 6
    assert len(domain.functions) == 4
    assert len(domain.actions) == 5


def test_parse_action_with_function_equality_precondition_sets_a_new_numeric_precondition():
    domain_parser = DomainParser(PLANT_WATERING_DOMAIN)
    domain = domain_parser.parse_domain()
    assert domain is not None
    assert len(domain.actions) == 10
    assert len(domain.actions["pour"].preconditions.root.operands) == 5
    for action in domain.actions.values():
        print(action.name)
        print(action.preconditions)


def test_parse_preconditions_with_action_with_disjunctive_preconditions_extracts_different_set_of_preconditions():
    test_action_str = """(lift
	:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
	:precondition (and (on ?y ?z) (at ?y ?p) (clear ?y) (at ?x ?p) (available ?x)
				(or (and		
    (>= (+ (* (fuel-cost ) -0.01) 0.78) 0.0)		
    (>= (+ (* (fuel-cost ) -0.02) 1.01) 0.0)		
    )		
    (and		
    (>= (+ (* (fuel-cost ) 0.01) -1.79) 0.0)		
    (>= (+ (+ (* (weight ?y) 0.01) (* (fuel-cost ) 0.01)) -2.05) 0.0)		
    (>= (+ (* (fuel-cost ) -0.01) 0.78) 0.0)		
    )))
        :effect (and (clear ?z) (lifting ?x ?y) (not (available ?x)) (not (on ?y ?z)) (not (at ?y ?p))
            (increase (fuel-cost ) 1.0)
    ))"""
    domain_parser = DomainParser(TEST_NUMERIC_DEPOT_DOMAIN_PATH)
    domain = domain_parser.parse_domain()
    action_tokens = PDDLTokenizer(pddl_str=test_action_str).parse()
    action = domain_parser.parse_action(action_tokens, domain.types, domain.functions, domain.predicates,
                                        domain.constants)
    preconditions = action.preconditions.root
    assert "(>= (+ 0.78 (* -0.01 (fuel-cost ))) 0.0)" in str(preconditions)
    assert "(>= (+ 1.01 (* -0.02 (fuel-cost ))) 0.0)" in str(preconditions)
    assert "(>= (+ -1.79 (* 0.01 (fuel-cost ))) 0.0)" in str(preconditions)
    assert "(>= (+ -2.05 (+ (* 0.01 (fuel-cost )) (* 0.01 (weight ?y)))) 0.0)" in str(preconditions)
    assert "(>= (+ 0.78 (* -0.01 (fuel-cost ))) 0.0)" in str(preconditions)
    assert "or" in str(preconditions)
    print(str(preconditions))


def test_parse_preconditions_with_action_with_universal_preconditions_works():
    test_action_str = """(lift
	:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
	:precondition (and  (at ?y ?p)
					    (not (lifting ?x ?y))
					    (forall (?y1 - crate) (and (at ?y1 ?p)))
				        (clear ?z))
        :effect (and (clear ?z) (lifting ?x ?y) (not (available ?x)) (not (on ?y ?z)) (not (at ?y ?p))
            (increase (fuel-cost ) 1.0)
    ))"""
    domain_parser = DomainParser(TEST_NUMERIC_DEPOT_DOMAIN_PATH)
    domain = domain_parser.parse_domain()
    action_tokens = PDDLTokenizer(pddl_str=test_action_str).parse()
    action = domain_parser.parse_action(action_tokens, domain.types, domain.functions, domain.predicates,
                                        domain.constants)
    preconditions = action.preconditions.root
    print(str(preconditions))


def test_parse_domain_with_domain_with_conditional_effects_not_fail():
    domain_parser = DomainParser(SPIDER_DOMAIN_PATH)
    domain = domain_parser.parse_domain()
    print(str(domain))


def test_parse_domain_nested_action_schema_does_not_fail():
    domain_parser = DomainParser(UMT2_DOMAIN_PATH)
    try:
        domain = domain_parser.parse_domain()
        for action in domain.actions.values():
            print(action.name)
            print(action.preconditions)
            print()
    except Exception:
        fail("Parsing domain with nested action schema failed.")


def test_parse_domain_with_nested_universal_preconditions_does_not_fail():
    domain_parser = DomainParser(MICONIC_LEARNED_DOMAIN_PATH)
    try:
        domain = domain_parser.parse_domain()
        for action in domain.actions.values():
            print(action.name)
            print(action.preconditions)
            print()
    except Exception:
        fail("Parsing domain with nested action schema failed.")
