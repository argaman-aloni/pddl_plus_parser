"""module to test the problem parsing functionality."""
from pytest import fixture, raises, fail

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, PDDLTokenizer
from pddl_plus_parser.models import Domain
from tests.lisp_parsers_tests.consts import (
    TEST_NUMERIC_DOMAIN,
    TEST_NUMERIC_PROBLEM,
    ZENOTRAVEL_DOMAIN_PATH,
    ZENOTRAVEL_PROBLEM_PATH,
)

test_objects_ast = [
    "num0",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
    "num9",
    "num10",
    "num11",
    "num12",
    "num13",
    "num14",
    "num15",
    "num16",
    "-",
    "num",
    "stage1",
    "stage2",
    "stage3",
    "stage4",
    "-",
    "stage",
    "round1",
    "round2",
    "round3",
    "round4",
    "round5",
    "round6",
    "round7",
    "round8",
    "round9",
    "round10",
    "-",
    "round",
    "worker1",
    "worker2",
    "worker3",
    "worker4",
    "-",
    "worker",
    "room1",
    "room2",
    "room3",
    "room4",
    "-",
    "room",
]


@fixture(scope="module")
def domain() -> Domain:
    domain_parser = DomainParser(TEST_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def zenotravel_domain() -> Domain:
    domain_parser = DomainParser(ZENOTRAVEL_DOMAIN_PATH)
    return domain_parser.parse_domain()


@fixture()
def zenotravel_problem_parser(zenotravel_domain: Domain):
    return ProblemParser(problem_path=ZENOTRAVEL_PROBLEM_PATH, domain=zenotravel_domain)


@fixture(scope="module")
def problem_parser(domain: Domain) -> ProblemParser:
    return ProblemParser(problem_path=TEST_NUMERIC_PROBLEM, domain=domain)


def set_objects_in_problem(problem_parser):
    parsed_objects = problem_parser.parse_objects(test_objects_ast)
    problem_parser.problem.objects = parsed_objects


@fixture()
def problem_parser_with_objects(domain: Domain) -> ProblemParser:
    problem_parser = ProblemParser(problem_path=TEST_NUMERIC_PROBLEM, domain=domain)
    parsed_objects = problem_parser.parse_objects(test_objects_ast)
    problem_parser.problem.objects = parsed_objects
    return problem_parser


def test_parse_domain_name_when_given_invalid_domain_name_raises_error(problem_parser):
    bad_domain_name = "bad-domain-name"
    with raises(ValueError):
        problem_parser.parse_domain_name(bad_domain_name)


def test_parse_domain_name_when_given_valid_domain_name_no_error_is_raised(
    problem_parser, domain: Domain
):
    try:
        problem_parser.parse_domain_name(domain.name)
    except ValueError:
        fail()


def test_parse_objects_parse_simple_objects_list_with_one_type_correctly(
    problem_parser,
):
    test_objects_ast = [
        "num1",
        "num2",
        "num3",
        "num4",
        "num5",
        "num6",
        "num7",
        "num8",
        "num9",
        "num10",
        "num11",
        "num12",
        "num13",
        "num14",
        "num15",
        "num16",
        "-",
        "num",
    ]
    parsed_objects = problem_parser.parse_objects(test_objects_ast)
    assert len(parsed_objects) == 16
    assert all([obj.type.name == "num" for obj in parsed_objects.values()])


def test_parse_objects_with_private_objects_parse_correctly_correctly(problem_parser):
    objects_str_with_private_objs = """(
    num0 num1 num2 num3  - num
    (:private
        stage1 stage2 - stage
        round1 round2  - round
    )
    worker1 worker2 - worker
    )
    """
    tokenizer = PDDLTokenizer(pddl_str=objects_str_with_private_objs)
    parsed_objects = problem_parser.parse_objects(tokenizer.parse())
    assert set(parsed_objects.keys()) == {
        "num0",
        "num1",
        "num2",
        "num3",
        "stage1",
        "stage2",
        "round1",
        "round2",
        "worker1",
        "worker2",
    }


def test_parse_objects_parse_objects_list_with_multiple_types_correctly(problem_parser):
    parsed_objects = problem_parser.parse_objects(test_objects_ast)
    objects_types = set([obj.type.name for obj in parsed_objects.values()])
    assert len(objects_types) == 5


def test_parse_grounded_numeric_fluent_with_different_number_of_parameters_than_domain_definition_raises_error(
    problem_parser,
):
    test_bad_function_ast = ["group_worker_cost", "worker2", "worker3"]
    with raises(ValueError):
        problem_parser.parse_grounded_numeric_fluent(test_bad_function_ast)


def test_parse_grounded_numeric_fluent_with_correct_number_parameters_and_bad_parameter_type_raises_error(
    problem_parser_with_objects: ProblemParser,
):
    test_bad_function_ast = ["group_worker_cost", "num8"]
    with raises(AssertionError):
        problem_parser_with_objects.parse_grounded_numeric_fluent(test_bad_function_ast)


def test_parse_grounded_numeric_fluent_wrong_function_name_raises_error(
    problem_parser_with_objects: ProblemParser,
):
    test_bad_function_ast = ["group_worker_cost-blah", "num8"]
    with raises(AssertionError):
        problem_parser_with_objects.parse_grounded_numeric_fluent(test_bad_function_ast)


def test_parse_grounded_numeric_fluent_with_valid_grounded_fluent_definition_return_the_function_object_generated(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    valid_grounded_function = ["group_worker_cost", "worker2"]
    extracted_function = problem_parser_with_objects.parse_grounded_numeric_fluent(
        valid_grounded_function
    )
    assert extracted_function.name == "group_worker_cost"
    assert extracted_function.signature == {"worker2": domain.types["worker"]}


def test_parse_grounded_numeric_fluent_with_valid_grounded_fluent_with_repeating_parameters_returns_correct_function(
    zenotravel_problem_parser: ProblemParser, zenotravel_domain: Domain
):
    valid_grounded_function = ["distance", "city7", "city7"]
    test_objects_ast = [f"city{i}" for i in range(0, 10)]
    test_objects_ast.extend(["-", "city"])

    parsed_objects = zenotravel_problem_parser.parse_objects(test_objects_ast)
    zenotravel_problem_parser.problem.objects = parsed_objects

    extracted_function = zenotravel_problem_parser.parse_grounded_numeric_fluent(
        valid_grounded_function
    )
    assert extracted_function.name == "distance"
    assert extracted_function.signature == {"city7": zenotravel_domain.types["city"]}
    assert extracted_function.state_representation == "(= (distance city7 city7) 0)"


def test_parse_parse_grounded_predicate_when_given_wrong_number_of_parameters_raises_an_error(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    invalid_predicate_wrong_num_params = ["next_num", "num0", "num1", "num2"]
    lifted_predicate = domain.predicates["next_num"]
    with raises(ValueError):
        problem_parser_with_objects.parse_grounded_predicate(
            invalid_predicate_wrong_num_params, lifted_predicate
        )


def test_parse_parse_grounded_predicate_when_given_wrong_parameter_type_raises_error(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    invalid_predicate_wrong_type = ["next_num", "num0", "stage4"]
    lifted_predicate = domain.predicates["next_num"]
    with raises(AssertionError):
        problem_parser_with_objects.parse_grounded_predicate(
            invalid_predicate_wrong_type, lifted_predicate
        )


def test_parse_grounded_predicate_with_legal_predicate_returns_grounded_predicate_object(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    valid_predicate = ["next_num", "num0", "num1"]
    test_predicate_name = "next_num"
    lifted_predicate = domain.predicates[test_predicate_name]
    grounded_predicate = problem_parser_with_objects.parse_grounded_predicate(
        valid_predicate, lifted_predicate
    )
    assert grounded_predicate is not None
    assert grounded_predicate.name == test_predicate_name
    assert grounded_predicate.signature == lifted_predicate.signature
    assert grounded_predicate.object_mapping == {"?i1": "num0", "?i2": "num1"}


def test_parse_grounded_predicate_with_legal_predicate_with_constant_returns_grounded_predicate_object(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    valid_predicate_with_const = ["harvest_phase", "stage3", "harvest_end"]
    test_predicate_name = "harvest_phase"
    lifted_predicate = domain.predicates[test_predicate_name]
    grounded_predicate = problem_parser_with_objects.parse_grounded_predicate(
        valid_predicate_with_const, lifted_predicate
    )
    assert grounded_predicate is not None
    assert grounded_predicate.name == test_predicate_name
    assert grounded_predicate.signature == lifted_predicate.signature
    assert grounded_predicate.object_mapping == {
        "?s": "stage3",
        "?hclass": "harvest_end",
    }


def test_parse_state_component_when_given_fluent_component_with_wrong_length_raises_error(
    problem_parser_with_objects: ProblemParser,
):
    invalid_fluent_state_component = [
        "=",
        ["group_worker_cost", "worker2"],
        "60",
        "70",
        "80",
    ]
    with raises(SyntaxError):
        problem_parser_with_objects.parse_state_component(
            invalid_fluent_state_component
        )


def test_parse_state_component_with_legal_fluent_set_fluent_value_to_the_input_float_value(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    valid_function_expression = ["=", ["group_worker_cost", "worker2"], "60"]
    problem_parser_with_objects.parse_state_component(valid_function_expression)

    expected_function_str = "(group_worker_cost worker2)"
    assert len(problem_parser_with_objects.problem.initial_state_fluents) == 1
    extracted_function = problem_parser_with_objects.problem.initial_state_fluents[
        expected_function_str
    ]
    assert extracted_function.value == 60


def test_parse_state_component_when_given_invalid_numeric_term_raises_error(
    problem_parser_with_objects: ProblemParser,
):
    invalid_fluent_state_component = ["*", ["group_worker_cost", "worker2"], "60"]
    with raises(ValueError):
        problem_parser_with_objects.parse_state_component(
            invalid_fluent_state_component
        )


def test_parse_state_component_when_given_invalid_predicate_term_raises_error(
    problem_parser_with_objects: ProblemParser,
):
    invalid_fluent_state_component = ["num_substract_blah", "num3", "num1", "num2"]
    with raises(ValueError):
        problem_parser_with_objects.parse_state_component(
            invalid_fluent_state_component
        )


def test_parse_state_component_with_legal_predicate_set_predicate_in_problem_data(
    problem_parser_with_objects: ProblemParser, domain: Domain
):
    valid_predicate = ["next_num", "num0", "num1"]
    test_predicate_name = "next_num"
    problem_parser_with_objects.parse_state_component(valid_predicate)
    expected_lifted_predicate = domain.predicates[
        test_predicate_name
    ].untyped_representation
    assert (
        expected_lifted_predicate
        in problem_parser_with_objects.problem.initial_state_predicates
    )


def test_parse_initial_state_with_single_component_does_not_fail(
    problem_parser_with_objects: ProblemParser,
):
    test_initial_state = [["num_substract", "num1", "num1", "num0"]]
    try:
        problem_parser_with_objects.parse_initial_state(test_initial_state)
    except Exception:
        fail()


def test_parse_initial_state_with_multiple_component_does_not_fail(
    problem_parser_with_objects: ProblemParser,
):
    test_complex_initial_state = [
        ["=", ["group_worker_cost", "worker2"], "60"],
        ["=", ["group_worker_cost", "worker3"], "30"],
        ["=", ["group_worker_cost", "worker4"], "15"],
        ["next_num", "num0", "num1"],
        ["next_num", "num1", "num2"],
        ["next_num", "num2", "num3"],
        ["next_num", "num3", "num4"],
        ["next_num", "num4", "num5"],
        ["next_num", "num5", "num6"],
        ["next_num", "num6", "num7"],
        ["next_num", "num7", "num8"],
        ["next_num", "num8", "num9"],
        ["next_num", "num9", "num10"],
        ["next_num", "num10", "num11"],
        ["next_num", "num11", "num12"],
        ["next_num", "num12", "num13"],
        ["next_num", "num13", "num14"],
        ["next_num", "num14", "num15"],
        ["next_num", "num15", "num16"],
        ["num_substract", "num1", "num1", "num0"],
        ["num_substract", "num2", "num1", "num1"],
        ["num_substract", "num2", "num2", "num0"],
        ["num_substract", "num3", "num1", "num2"],
        ["num_substract", "num3", "num2", "num1"],
        ["num_substract", "num3", "num3", "num0"],
        ["num_substract", "num4", "num1", "num3"],
        ["num_substract", "num4", "num2", "num2"],
        ["num_substract", "num4", "num3", "num1"],
        ["num_substract", "num4", "num4", "num0"],
        ["num_substract", "num5", "num1", "num4"],
        ["num_substract", "num5", "num2", "num3"],
        ["num_substract", "num5", "num3", "num2"],
        ["num_substract", "num5", "num4", "num1"],
        ["num_substract", "num5", "num5", "num0"],
        ["num_substract", "num6", "num1", "num5"],
        ["num_substract", "num6", "num2", "num4"],
        ["num_substract", "num6", "num3", "num3"],
        ["num_substract", "num6", "num4", "num2"],
        ["num_substract", "num6", "num5", "num1"],
        ["num_substract", "num6", "num6", "num0"],
        ["num_substract", "num7", "num1", "num6"],
        ["num_substract", "num7", "num2", "num5"],
        ["num_substract", "num7", "num3", "num4"],
        ["num_substract", "num7", "num4", "num3"],
        ["num_substract", "num7", "num5", "num2"],
        ["num_substract", "num7", "num6", "num1"],
        ["num_substract", "num7", "num7", "num0"],
        ["num_substract", "num8", "num1", "num7"],
        ["num_substract", "num8", "num2", "num6"],
        ["num_substract", "num8", "num3", "num5"],
        ["num_substract", "num8", "num4", "num4"],
        ["num_substract", "num8", "num5", "num3"],
        ["num_substract", "num8", "num6", "num2"],
        ["num_substract", "num8", "num7", "num1"],
        ["num_substract", "num8", "num8", "num0"],
        ["num_substract", "num9", "num1", "num8"],
        ["num_substract", "num9", "num2", "num7"],
        ["num_substract", "num9", "num3", "num6"],
        ["num_substract", "num9", "num4", "num5"],
        ["num_substract", "num9", "num5", "num4"],
    ]
    try:
        problem_parser_with_objects.parse_initial_state(test_complex_initial_state)
    except Exception:
        fail()


def test_parse_goal_state_when_parsing_ast_that_does_not_start_with_and_raises_error(
    problem_parser_with_objects: ProblemParser,
):
    bad_goal_state = ["blah", ["harvest_phase", "stage3", "harvest_end"]]
    with raises(SyntaxError):
        problem_parser_with_objects.parse_goal_state(bad_goal_state)


def test_parse_goal_state_when_parsing_simple_numeric_condition_the_numeric_tree_is_created_correctly(
    problem_parser_with_objects: ProblemParser,
):
    goal_state_numeric_tokens = PDDLTokenizer(
        pddl_str="(and (not (next_num num12 num13)))"
    ).parse()
    problem_parser_with_objects.parse_goal_state(goal_state_numeric_tokens)
    assert len(problem_parser_with_objects.problem.goal_state_predicates) == 1
    for predicate in problem_parser_with_objects.problem.goal_state_predicates:
        print(predicate)


def test_parse_goal_state_when_parsing_negative_goal_statement_should_not_fail_and_return_correct_goal(
    problem_parser_with_objects: ProblemParser,
):
    goal_state_numeric_tokens = PDDLTokenizer(
        pddl_str="(and (>= (group_worker_cost worker1) 1))"
    ).parse()
    problem_parser_with_objects.parse_goal_state(goal_state_numeric_tokens)
    assert len(problem_parser_with_objects.problem.goal_state_fluents) == 1
    for fluent in problem_parser_with_objects.problem.goal_state_fluents:
        print(fluent)


def test_parse_goal_state_when_parsing_complex_numeric_condition_the_numeric_tree_is_created_correctly(
    problem_parser_with_objects: ProblemParser,
):
    goal_state_numeric_tokens = PDDLTokenizer(
        pddl_str="(and (>= (+ (* 2.0 (group_worker_cost worker0)) "
        "(+ (* 1.0 (group_worker_cost worker1)) (+ (* 1.5 (group_worker_cost worker2)) 0))) 14.0))"
    ).parse()
    problem_parser_with_objects.parse_goal_state(goal_state_numeric_tokens)
    assert len(problem_parser_with_objects.problem.goal_state_fluents) == 1
    for fluent in problem_parser_with_objects.problem.goal_state_fluents:
        print(fluent)


def test_parse_goal_state_when_parsing_multiple_numeric_conditions_the_numeric_tree_is_created_correctly(
    problem_parser_with_objects: ProblemParser,
):
    goal_state_numeric_tokens = PDDLTokenizer(
        pddl_str="""(and
			(>= (group_worker_cost worker0) 1)
			(>= (group_worker_cost worker1) 1)
			(>= (group_worker_cost worker2) 1)
			(>= (+ (* 2.0 (group_worker_cost worker0))(+ (* 1.0 (group_worker_cost worker1))(+ (* 1.5 (group_worker_cost worker2)) 0))) 14.0)
		)"""
    ).parse()

    problem_parser_with_objects.parse_goal_state(goal_state_numeric_tokens)
    assert len(problem_parser_with_objects.problem.goal_state_fluents) == 4
    for fluent in problem_parser_with_objects.problem.goal_state_fluents:
        print(fluent)


def test_parse_goal_state_with_legal_goal_state_extract_correct_number_of_grounded_predicates(
    problem_parser_with_objects: ProblemParser,
):
    valid_goal_state = ["and", ["harvest_phase", "stage3", "harvest_end"]]
    problem_parser_with_objects.parse_goal_state(valid_goal_state)
    assert len(problem_parser_with_objects.problem.goal_state_predicates) == 1


def test_parse_problem_with_real_problem_data_does_not_fail(problem_parser):
    try:
        problem = problem_parser.parse_problem()
        print(problem)
    except Exception:
        fail()
