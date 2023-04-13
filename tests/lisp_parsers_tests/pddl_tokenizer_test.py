from pddl_plus_parser.lisp_parsers import PDDLTokenizer
from tests.lisp_parsers_tests.consts import TEST_NUMERIC_PROBLEM


def test_simple_parsing():
    test_program = "(begin (define r 10) (* pi (* r r)))"
    simple_lisp_parser = PDDLTokenizer(pddl_str=test_program)
    tokens = simple_lisp_parser.parse()
    assert tokens == ['begin', ['define', 'r', '10'], ['*', 'pi', ['*', 'r', 'r']]]


def test_simple_predicate_tokenization():
    test_predicate = "(available ?obj - woodobj)"
    simple_lisp_parser = PDDLTokenizer(pddl_str=test_predicate)
    tokens = simple_lisp_parser.parse()
    assert tokens == ['available', '?obj', '-', 'woodobj']


def test_multiple_predicates_tokenization():
    test_predicates = """((available ?obj - woodobj)
    (surface-condition ?obj - woodobj ?surface - surface))"""
    multi_predicate_tokenizer = PDDLTokenizer(pddl_str=test_predicates)
    tokens = multi_predicate_tokenizer.parse()
    assert tokens == [['available', '?obj', '-', 'woodobj'],
                      ['surface-condition', '?obj', '-', 'woodobj', '?surface', '-', 'surface']]


def test_parse_action_yields_correct_action_ast():
    test_action_str = """(do-spray-varnish
    	:parameters   (?m - spray-varnisher ?x - part ?newcolour - acolour ?surface - surface)
    	:precondition (and (available ?x) (has-colour ?m ?newcolour))
    	:effect       (and (treatment ?x varnished) (colour ?x ?newcolour)))"""
    multi_predicate_tokenizer = PDDLTokenizer(pddl_str=test_action_str)
    tokens = multi_predicate_tokenizer.parse()
    expected_tokens = ['do-spray-varnish',
                       ':parameters',
                       ['?m', '-', 'spray-varnisher', '?x', '-', 'part', '?newcolour', '-', 'acolour', '?surface', '-',
                        'surface'],
                       ':precondition', ['and', ['available', '?x'], ['has-colour', '?m', '?newcolour']],
                       ':effect', ['and', ['treatment', '?x', 'varnished'], ['colour', '?x', '?newcolour']]]
    assert tokens == expected_tokens


def test_parse_simple_numeric_inequality_expression():
    test_expression = "(>= (height-cap-l ?des) (height-v ?v))"
    expression_tokenizer = PDDLTokenizer(pddl_str=test_expression)
    tokens = expression_tokenizer.parse()
    expected_tokens = ['>=', ['height-cap-l', '?des'], ['height-v', '?v']]
    assert tokens == expected_tokens


def test_parse_simple_numeric_equality_expression():
    test_expression = "(= (height-cap-l ?des) (height-v ?v))"
    expression_tokenizer = PDDLTokenizer(pddl_str=test_expression)
    tokens = expression_tokenizer.parse()
    expected_tokens = ['=', ['height-cap-l', '?des'], ['height-v', '?v']]
    assert tokens == expected_tokens


def test_parse_simple_object_equality_expression():
    test_expression = "(= ?ori ?des)"
    expression_tokenizer = PDDLTokenizer(pddl_str=test_expression)
    tokens = expression_tokenizer.parse()
    expected_tokens = ['=', '?ori', '?des']
    assert tokens == expected_tokens


def test_parse_simple_existential_expression():
    test_expression = "(exists (?p - package) (and (at-packagev ?p ?v)))"
    expression_tokenizer = PDDLTokenizer(pddl_str=test_expression)
    tokens = expression_tokenizer.parse()
    expected_tokens = ['exists', ['?p', '-', 'package'], ['and', ['at-packagev', '?p', '?v']]]
    assert tokens == expected_tokens


def test_parse_problem():
    test_problem_tokenizer = PDDLTokenizer(file_path=TEST_NUMERIC_PROBLEM)
    print(test_problem_tokenizer.parse())
