"""Module containing a parser that is able to parse PDDL domains."""
import logging
from collections import Counter
from pathlib import Path
from typing import NoReturn, List, Union, Dict

from pddl_plus_parser.lisp_parsers import PDDLTokenizer
from pddl_plus_parser.models import Domain, PDDLObject, Problem, PDDLFunction, Predicate, GroundedPredicate, \
    NumericalExpressionTree, construct_expression_tree

LEGAL_GOAL_OPERATORS = [">", "=", "<", ">=", "<="]


class ProblemParser:
    """Class that parses PDDL+ problem files."""

    tokenizer: PDDLTokenizer
    logger: logging.Logger
    domain: Domain
    problem: Problem

    def __init__(self, problem_path: Path, domain: Domain):
        self.tokenizer = PDDLTokenizer(problem_path)
        self.domain = domain
        self.logger = logging.getLogger(__name__)
        self.problem = Problem(domain)

    def _validate_object_types(self, lifted_predicate: Predicate, predicate_signature_items: List[str]) -> NoReturn:
        """Validate that the grounded predicate objects match the lifted predicate signature's type.

        :param lifted_predicate: the lifted predicate that is being compared to.
        :param predicate_signature_items: the objects of the grounded predicate AST.
        """
        optional_objects = {name: pddl_object for name, pddl_object in self.problem.objects.items()}
        optional_objects.update(self.domain.constants)
        objects_types = [optional_objects[obj_name].type for obj_name in predicate_signature_items]
        lifted_predicate_types = list(lifted_predicate.signature.values())
        for index, grounded_object_type in enumerate(objects_types):
            assert grounded_object_type.is_sub_type(lifted_predicate_types[index])

    def parse_domain_name(self, domain_name: str) -> NoReturn:
        """Parse the domain name in the problem file and verifies that the name given matches the inner domain.

        :param domain_name: the name of the domain given as input.
        """
        self.logger.info("Parsing the name of the domain given in the problem definition.")
        if domain_name != self.domain.name:
            raise ValueError(f"Given a problem with mismatching domain. "
                             f"Given domain name - {domain_name} problem domain - {self.domain.name}")

    def parse_objects(self, objects_ast: List[str]) -> Dict[str, PDDLObject]:
        """Parses the objects in the problem definition.

        :param objects_ast: the list of strings representing the typed objects in the problem.
        :return: the list of PDDL objects that are defined in the PDDL problem.
        """
        self.logger.info("Starting to parse the problem's objects.")
        problem_objects = {}
        same_type_objects = []
        iterator = 0
        while iterator < len(objects_ast):
            if isinstance(objects_ast[iterator], list):
                self.logger.debug("Found private objects, iterating over them and then continue regularly.")
                private_objects = self.parse_objects(objects_ast[iterator][1:])
                problem_objects.update(private_objects)
                iterator += 1
                continue

            if objects_ast[iterator] != "-":
                same_type_objects.append(objects_ast[iterator])
                iterator += 1
                continue

            objects_type = objects_ast[iterator + 1]
            if objects_type not in self.domain.types:
                raise ValueError(f"Received illegal objects type - {objects_type}")

            problem_objects.update(
                {name: PDDLObject(name=name, type=self.domain.types[objects_type]) for name in same_type_objects})
            same_type_objects = []
            iterator += 2
            continue

        return problem_objects

    def parse_grounded_numeric_fluent(self, grounded_numeric_fluent: List[str]) -> PDDLFunction:
        """Parse a single grounded numeric fluent in the problem.

        :param grounded_numeric_fluent: the grounded fluent that is present in the problem.
        :return: the function object representing the grounded fluent.
        """
        function_name = grounded_numeric_fluent[0]
        self.logger.info(f"Starting to parse the grounded numeric fluent - {function_name}")
        assert function_name in self.domain.functions
        lifted_function = self.domain.functions[function_name]
        # For now, assuming that fluents have valid parameters.
        fluent_signature_items = grounded_numeric_fluent[1:]
        grounded_fluents_counter = Counter(fluent_signature_items)
        if len(fluent_signature_items) != len(lifted_function.signature):
            raise ValueError(f"Received fluent - {function_name} with wrong number of parameters! "
                             f"Expected - {len(lifted_function.signature)} and received - {len(fluent_signature_items)}")

        possible_objects = {**self.problem.objects, **self.domain.constants}
        fluent_signature = {
            object_name: possible_objects[object_name].type for object_name in fluent_signature_items
        }
        repeating_items = {object_name: count for object_name, count in grounded_fluents_counter.items() if count > 1}
        for grounded_signature_type, lifted_signature_type in zip(fluent_signature.values(),
                                                                  lifted_function.signature.values()):
            assert grounded_signature_type.is_sub_type(lifted_signature_type)

        return PDDLFunction(name=function_name, signature=fluent_signature, repeating_variables=repeating_items)

    def parse_grounded_predicate(self, grounded_predicate_ast: List[str],
                                 lifted_predicate: Predicate) -> GroundedPredicate:
        """Parse the grounded predicate that appears in the problem definition.

        :param grounded_predicate_ast: the AST that represents the grounded predicate.
        :param lifted_predicate: the lifted predicate that the domain defines.
        :return: the grounded predicate represented by the lifted predicate.
        """
        predicate_name = lifted_predicate.name
        predicate_signature_items = grounded_predicate_ast[1:]
        self.logger.info(f"Starting the parse the grounded predicate - {predicate_name} "
                         f"with the signature - {predicate_signature_items}.")
        if len(predicate_signature_items) != len(lifted_predicate.signature):
            raise ValueError(
                f"Received illegal grounded predicate with mismatching signature - {grounded_predicate_ast}")

        self._validate_object_types(lifted_predicate, predicate_signature_items)
        object_mapping = {
            parameter_name: object_name for object_name, parameter_name in
            zip(predicate_signature_items, lifted_predicate.signature)
        }

        return GroundedPredicate(name=predicate_name, signature=lifted_predicate.signature,
                                 object_mapping=object_mapping)

    def parse_state_component(self, expression: List[Union[str, List[str]]]) -> NoReturn:
        """Parse a single AST component that represents either a predicate or a numeric fluent.

        :param expression: the ast component that can represent either a predicate or a numeric fluent.
        """
        self.logger.info("Parsing a single component from the initial state data.")
        if expression[0] == "=":  # This is an assignment of a grounded numeric fluent.
            if len(expression) != 3:  # ['=', <function items as a list>, '<value>']
                raise SyntaxError("A numeric fluent should be of length 3. Fluent scheme: "
                                  "(= (<fluent_name> <argument>) <value>)"
                                  f"Received - {expression}")

            self.logger.debug("Component found is a numeric fluent, starting to process the fluent.")
            function_data = expression[1]
            assigned_value = float(expression[2])
            numeric_fluent = self.parse_grounded_numeric_fluent(function_data)
            self.logger.debug(f"Setting the fluent's value to - {assigned_value}")
            numeric_fluent.set_value(assigned_value)
            self.problem.initial_state_fluents[numeric_fluent.untyped_representation] = numeric_fluent
            return

        if expression[0] in self.domain.predicates:
            self.logger.debug("Component found is a predicate, starting to process it.")
            lifted_predicate = self.domain.predicates[expression[0]]
            grounded_predicate = self.parse_grounded_predicate(expression, lifted_predicate)
            self.problem.initial_state_predicates[lifted_predicate.untyped_representation].add(grounded_predicate)
            return

        raise ValueError(f"Received illegal state component - {expression}")

    def parse_initial_state(self, init_ast: List[List[Union[str, List[str]]]]) -> NoReturn:
        """Parse the initial state of the problem.

        :param init_ast: the AST representation of the inital state.
        """
        self.logger.info("Starting to parse the initial state!")
        for expression in init_ast:
            self.parse_state_component(expression)

    def parse_goal_state(self, goal_state_ast: List[List[Union[str, List[str]]]]) -> NoReturn:
        """Parse the goal state of the problem and extracts the list of grounded predicates from it.

        :param goal_state_ast: the AST representation of the goal state.
        """
        if goal_state_ast[0] != "and":
            raise SyntaxError("Goal state should always start with an AND statement!")

        for expression in goal_state_ast[1:]:
            if expression[0] not in self.domain.predicates and expression[0] not in LEGAL_GOAL_OPERATORS:
                raise ValueError(f"Received illegal state component - {expression}")

            if expression[0] not in LEGAL_GOAL_OPERATORS:  # This is an assignment of a grounded numeric fluent.
                grounded_predicate = self.parse_grounded_predicate(expression, self.domain.predicates[expression[0]])
                self.problem.goal_state_predicates.append(grounded_predicate)
                continue

            numeric_goal_statement = NumericalExpressionTree(
                construct_expression_tree(expression, self.domain.functions))
            self.problem.goal_state_fluents.add(numeric_goal_statement)

    def parse_problem(self) -> Problem:
        """Parse the problem's AST and extracts the object that is represented by the input scheme.

        :return: the problem object.
        """
        problem_expression = self.tokenizer.parse()
        if problem_expression[0] != "define":
            raise SyntaxError("Encountered a PDDL that does not start with 'define' statement!")

        for macro_expression in problem_expression:
            if macro_expression[0] == "problem":
                self.problem.name = macro_expression[1]
                continue

            elif macro_expression[0] == ":domain":
                self.parse_domain_name(macro_expression[1])
                continue

            elif macro_expression[0] == ":objects":
                self.problem.objects = self.parse_objects(macro_expression[1:])

            elif macro_expression[0] == ":init":
                self.parse_initial_state(macro_expression[1:])
                continue

            elif macro_expression[0] == ":goal":
                self.parse_goal_state(macro_expression[1])
                continue

            elif macro_expression == ":metric":
                self.logger.debug("Currently not parsing the metric section of the problem.")
                continue

        return self.problem
