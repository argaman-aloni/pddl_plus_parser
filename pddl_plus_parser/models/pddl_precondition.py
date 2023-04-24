"""Module containing the classes representing the preconditions of a PDDL+ action."""
from typing import Union, Set, Tuple

from pddl_plus_parser.models.numerical_expression import NumericalExpressionTree
from pddl_plus_parser.models.pddl_predicate import Predicate, GroundedPredicate
from pddl_plus_parser.models.pddl_type import PDDLType


class Precondition:
    """class representing a single precondition in a PDDL+ action."""
    binary_operator: str
    operands: Set[Union["Precondition", Predicate, NumericalExpressionTree]]
    equality_preconditions: Set[Tuple[str, str]]
    inequality_preconditions: Set[Tuple[str, str]]

    def __init__(self, binary_operator: str):
        self.binary_operator = binary_operator
        self.operands = set()
        self.equality_preconditions = set()
        self.inequality_preconditions = set()

    def _print_self(self) -> str:
        """Print the precondition in a human-readable format."""
        combined_preconditions = []
        for operand in self.operands:
            if isinstance(operand, Precondition):
                combined_preconditions.append(str(operand))

            elif isinstance(operand, Predicate):
                combined_preconditions.append(operand.untyped_representation)

            elif isinstance(operand, NumericalExpressionTree):
                combined_preconditions.append(operand.to_pddl())

        combined_conditions = "\n\t".join(combined_preconditions)
        equality_conditions = "\n\t".join([f"(= {o1} {o2})" for o1, o2 in self.equality_preconditions])
        inequality_conditions = "\n\t".join([f"(not (= {o1} {o2}))" for o1, o2 in self.inequality_preconditions])
        return f"({self.binary_operator} {combined_conditions}{equality_conditions}{inequality_conditions})"

    def _validate_equality(self, other: "Precondition") -> bool:
        """Validates if the two preconditions are logically equivalent.

        :param other: the other precondition to compare to.
        """
        if self.binary_operator != other.binary_operator:
            return False

        self_nested_conditions = [cond for cond in self.operands if isinstance(cond, Precondition)]
        self_primitive_predicates = {cond.untyped_representation for cond in self.operands if
                                     isinstance(cond, Predicate)}
        self_primitive_numeric_conditions = {cond.to_pddl() for cond in self.operands if
                                             isinstance(cond, NumericalExpressionTree)}

        other_nested_conditions = [cond for cond in other.operands if isinstance(cond, Precondition)]
        other_primitive_predicates = {cond.untyped_representation for cond in other.operands if
                                      isinstance(cond, Predicate)}
        other_primitive_numeric_conditions = {cond.to_pddl() for cond in other.operands if
                                              isinstance(cond, NumericalExpressionTree)}
        if self_primitive_predicates != other_primitive_predicates:
            return False
        if self_primitive_numeric_conditions != other_primitive_numeric_conditions:
            return False

        for nested_condition in self_nested_conditions:
            matched_condition = None
            for other_condition in other_nested_conditions:
                if nested_condition == other_condition:
                    matched_condition = other_condition
                    break

            if not matched_condition:
                return False

            other_nested_conditions.remove(matched_condition)

        return True

    def __str__(self):
        return self._print_self()

    def __iter__(self) -> Tuple[str, Union["Precondition", Predicate, GroundedPredicate, NumericalExpressionTree]]:
        for operand in self.operands:
            if isinstance(operand, Precondition):
                yield from operand
            else:
                yield self.binary_operator, operand

    def __eq__(self, other: "Precondition") -> bool:
        return self.binary_operator == other.binary_operator and \
            self.operands == other.operands and \
            self.equality_preconditions == other.equality_preconditions and \
            self.inequality_preconditions == other.inequality_preconditions

    def __hash__(self) -> int:
        return hash(str(self))

    def add_condition(self,
                      condition: Union["Precondition", Predicate, GroundedPredicate, NumericalExpressionTree]) -> None:
        """Add a condition to the precondition.

        :param condition: the condition to add.
        """
        if isinstance(condition, (Predicate, GroundedPredicate)):
            current_predicates = [cond.untyped_representation for cond in self.__iter__() if
                                  isinstance(cond, Predicate)]
            if condition.untyped_representation not in current_predicates:
                self.operands.add(condition)
        elif isinstance(condition, NumericalExpressionTree):
            current_expressions = [cond.to_pddl() for cond in self.__iter__() if
                                   isinstance(cond, NumericalExpressionTree)]
            if condition.to_pddl() not in current_expressions:
                self.operands.add(condition)
        else:
            current_compound_conditions = [str(cond) for cond in self.__iter__() if isinstance(cond, Precondition)]
            if str(condition) not in current_compound_conditions:
                self.operands.add(condition)

    def add_equality_condition(self, condition: Tuple[str, str], inequality: bool = False) -> None:
        """Add an equality condition to the precondition.

        :param condition: the equality condition to add
        :param inequality: whether the condition is an inequality
        """
        if not inequality:
            self.equality_preconditions.add(condition)
        else:
            self.inequality_preconditions.add(condition)


class UniversalPrecondition(Precondition):
    """Class representing a universally quantified precondition."""

    quantified_parameter: str
    quantified_type: PDDLType

    def __init__(self, quantified_parameter: str, quantified_type: PDDLType, binary_operator: str = "and"):
        self.quantified_parameter = quantified_parameter
        self.quantified_type = quantified_type
        super().__init__(binary_operator)

    def __str__(self):
        return f"(forall ({self.quantified_parameter} - {self.quantified_type.name})" \
               f"\n\t{super()._print_self()})"

    def __eq__(self, other: "UniversalPrecondition") -> bool:
        return super().__eq__(other) and \
            self.quantified_parameter == other.quantified_parameter and \
            self.quantified_type == other.quantified_type


class CompoundPrecondition:
    """class representing a single precondition in a PDDL+ action."""
    root: Union[Precondition, UniversalPrecondition]

    def __init__(self):
        self.root = Precondition("and")

    def __str__(self):
        return str(self.root)

    def __iter__(self) -> Tuple[str, Union[Precondition, UniversalPrecondition]]:
        yield from self.root

    def __eq__(self, other: "CompoundPrecondition") -> bool:
        return self.root == other.root
