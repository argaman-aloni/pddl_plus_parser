"""Module to parse a serialized trajectory and export it as an object fitted for learning."""
import logging
from collections import defaultdict
from pathlib import Path
from typing import List, Union

from pddl_plus_parser.lisp_parsers.pddl_tokenizer import PDDLTokenizer
from pddl_plus_parser.models import Domain, Observation, State, ActionCall, PDDLFunction, Predicate, GroundedPredicate, Problem


class TrajectoryParser:
    """Class that is able to parse a trajectory file and extract its content.

    Note: This class assumes that the trajectory size is tractable and thus, reads the entire file at once.
    For lay loading of a trajectory future development is needed.
    """

    partial_domain: Domain  # domain containing only the publicly known information.
    problem: Problem
    logger: logging.Logger

    def __init__(self, partial_domain: Domain, problem: Problem):
        self.partial_domain = partial_domain
        self.problem = problem
        self.logger = logging.getLogger(__name__)

    def _read_trajectory_file(self, trajectory_file_path: Path) -> PDDLTokenizer:
        """Reads the trajectory file and exports the lines containing the data about the trajectory.

        :param trajectory_file_path: the path to the trajectory file.
        :return: the tokenizer that is able to parse the trajectory strings to expressions.
        """
        self.logger.debug(f"Reading the file - {trajectory_file_path}")
        return PDDLTokenizer(file_path=trajectory_file_path)

    def parse_state(self, state_data: List[List[Union[str, List[str]]]]) -> State:
        """Parse the trajectory's state data and extracts the state.

        :param state_data: the AST representing the state.
        :return: the state object.
        """
        self.logger.info("Parsing the observed state.")
        state_predicates = defaultdict(set)
        state_fluents = {}
        for expression in state_data:
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
                state_fluents[numeric_fluent.untyped_representation] = numeric_fluent
                continue

            if expression[0] in self.partial_domain.predicates:
                self.logger.debug("Component found is a predicate, starting to process it.")
                lifted_predicate = self.partial_domain.predicates[expression[0]]
                grounded_predicate = self.parse_grounded_predicate(expression, lifted_predicate)
                state_predicates[lifted_predicate.untyped_representation].add(grounded_predicate)
                continue

            raise ValueError(f"Received illegal state component - {expression}")

        return State(predicates=state_predicates, fluents=state_fluents)

    def parse_grounded_numeric_fluent(self, grounded_numeric_fluent: List[str]) -> PDDLFunction:
        """Parse a single grounded numeric fluent in the problem.

        :param grounded_numeric_fluent: the grounded fluent that is present in the problem.
        :return: the function object representing the grounded fluent.
        """
        function_name = grounded_numeric_fluent[0]
        self.logger.info(f"Starting to parse the grounded numeric fluent - {function_name}")
        assert function_name in self.partial_domain.functions
        lifted_function = self.partial_domain.functions[function_name]
        # For now, assuming that fluents have valid parameters.
        fluent_signature_items = grounded_numeric_fluent[1:]
        if len(fluent_signature_items) != len(lifted_function.signature):
            raise ValueError(
                f"Received fluent - {function_name} with wrong number of parameters! "
                f"Expected - {len(lifted_function.signature)} and received - {len(fluent_signature_items)}")

        fluent_signature = {
            object_name: self.problem.objects[object_name].type for object_name in fluent_signature_items
        }
        for grounded_param_type, lifted_param_type in zip(fluent_signature.values(), lifted_function.signature.values()):
            assert grounded_param_type.is_sub_type(lifted_param_type)

        return PDDLFunction(name=function_name, signature=fluent_signature)

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

        object_mapping = {
            parameter_name: object_name for object_name, parameter_name in
            zip(predicate_signature_items, lifted_predicate.signature)
        }

        return GroundedPredicate(name=predicate_name, signature=lifted_predicate.signature,
                                 object_mapping=object_mapping)

    def parse_action_call(self, action_call_ast: List[List[str]]) -> ActionCall:
        """Parse the grounded action call in the trajectory.

        :param action_call_ast: a grounded action call in the form: [(<name> <p1> <p2> ... <pn>)]
        :return: the action call object.
        """
        self.logger.debug(f"Parsing the grounded action call - {action_call_ast}")
        action_call_data = action_call_ast[0]
        return ActionCall(name=action_call_data[0], grounded_parameters=action_call_data[1:])

    def parse_trajectory(self, trajectory_file_path: Path) -> Observation:
        """Parse a trajectory and extracts the observed data into objects.

        :param trajectory_file_path: the path to the trajectory file.
        :return: the observation extracted from the serialized trajectory.
        """
        self.logger.info("Starting to read the trajectory file!")
        tokenizer = self._read_trajectory_file(trajectory_file_path)
        observation_expression = tokenizer.parse()
        observation = Observation()
        self.logger.debug("Starting to generate the observation from the input trajectory.")
        for index in range(0, len(observation_expression) - 2, 2):
            macro_expression = observation_expression[index]
            if macro_expression[0] == ":init" or macro_expression[0] == ":state":
                previous_state = self.parse_state(macro_expression[1:])
                macro_expression = observation_expression[index + 1]
                if macro_expression[0] == "operator:":  # TODO: Still need to develop multiple action call mechanism
                    action_call = self.parse_action_call(macro_expression[1:])

                else:
                    raise SyntaxError("Encountered a trajectory without an action call!")

                macro_expression = observation_expression[index + 2]
                if macro_expression[0] != ":state":
                    raise SyntaxError("Encountered a trajectory without a next state!")

                next_state = self.parse_state(macro_expression[1:])
                self.logger.debug("Finished parsing a trajectory component.")
                observation.add_component(previous_state, action_call, next_state)

        return observation
