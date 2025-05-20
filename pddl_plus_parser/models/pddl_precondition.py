"""Module containing the classes representing the preconditions of a PDDL+ action."""
from typing import Union, Set, Tuple, List, Dict

from pddl_plus_parser.models.numeric_symbolic_operations import (
    simplify_inequality,
    simplify_equality,
)
from pddl_plus_parser.models.numerical_expression import NumericalExpressionTree
from pddl_plus_parser.models.pddl_predicate import Predicate, GroundedPredicate
from pddl_plus_parser.models.pddl_type import PDDLType

DEFAULT_DECIMAL_DIGITS = 2


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

    def _print_self(self, decimal_digits: int = DEFAULT_DECIMAL_DIGITS) -> str:
        """Print the precondition in a human-readable format.

        :param decimal_digits: the number of decimal digits to keep.
        """
        discrete_preconditions = []
        compound_preconditions = []
        numeric_expressions = []
        for operand in self.operands:
            if isinstance(operand, Precondition):
                compound_preconditions.append(str(operand))

            elif isinstance(operand, Predicate):
                discrete_preconditions.append(operand.untyped_representation)

            elif isinstance(operand, NumericalExpressionTree):
                numeric_expressions.append(operand)

        numeric_preconditions = [
            operand.to_pddl(decimal_digits) for operand in numeric_expressions
        ]

        discrete_preconditions.sort()
        numeric_preconditions = list(set(numeric_preconditions))  # remove duplicates
        numeric_preconditions.sort()
        compound_preconditions.sort()
        compound_preconditions = (
            discrete_preconditions + numeric_preconditions + compound_preconditions
        )
        combined_conditions = "\n\t".join(compound_preconditions)
        equality_conditions = "\n\t".join(
            [f"(= {o1} {o2})" for o1, o2 in self.equality_preconditions]
        )
        inequality_conditions = "\n\t".join(
            [f"(not (= {o1} {o2}))" for o1, o2 in self.inequality_preconditions]
        )
        return f"({self.binary_operator} {combined_conditions}{equality_conditions}{inequality_conditions})"

    def _validate_equality(self, other: "Precondition") -> bool:
        """Validates if the two preconditions are logically equivalent.

        :param other: the other precondition to compare to.
        """
        if self.binary_operator != other.binary_operator:
            return False

        self_nested_conditions = [
            cond for cond in self.operands if isinstance(cond, Precondition)
        ]
        self_primitive_predicates = {
            cond.untyped_representation
            for cond in self.operands
            if isinstance(cond, Predicate)
        }
        self_primitive_numeric_conditions = {
            cond.to_pddl()
            for cond in self.operands
            if isinstance(cond, NumericalExpressionTree)
        }

        other_nested_conditions = [
            cond for cond in other.operands if isinstance(cond, Precondition)
        ]
        other_primitive_predicates = {
            cond.untyped_representation
            for cond in other.operands
            if isinstance(cond, Predicate)
        }
        other_primitive_numeric_conditions = {
            cond.to_pddl()
            for cond in other.operands
            if isinstance(cond, NumericalExpressionTree)
        }
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

    def print(self, decimal_digits: int = DEFAULT_DECIMAL_DIGITS) -> str:
        """Print the precondition in a human-readable format.

        :param decimal_digits: the number of decimal digits to keep.
        """
        return self._print_self(decimal_digits)

    def __iter__(
        self,
    ) -> Tuple[
        str,
        Union["Precondition", Predicate, GroundedPredicate, NumericalExpressionTree],
    ]:
        for operand in self.operands:
            if isinstance(operand, Precondition):
                yield from operand

            else:
                yield self.binary_operator, operand

    def __eq__(self, other: "Precondition") -> bool:
        return (
            self.binary_operator == other.binary_operator
            and self.operands == other.operands
            and self.equality_preconditions == other.equality_preconditions
            and self.inequality_preconditions == other.inequality_preconditions
        )

    def __hash__(self) -> int:
        return hash(str(self))

    def __contains__(
        self,
        item: Union[
            "Precondition", Predicate, GroundedPredicate, NumericalExpressionTree
        ],
    ) -> bool:
        if len(self.operands) == 0:
            return False

        if item in self.operands:
            return True

        for operand in self.operands:
            if isinstance(operand, Precondition):
                if item in operand:
                    return True

        return False

    def _unique_add_predicate(
        self, condition: Union[Predicate, GroundedPredicate]
    ) -> None:
        """Adds a new predicate to the precondition if it does not already exist.

        :param condition: the condition to add.
        """
        current_predicates = [
            cond.untyped_representation
            for _, cond in self.__iter__()
            if isinstance(cond, Predicate)
        ]
        if condition.untyped_representation not in current_predicates:
            self.operands.add(condition)

    def _unique_add_numeric_expression(
        self, condition: NumericalExpressionTree
    ) -> None:
        """Adds a new numeric expression to the precondition if it does not already exist.

        :param condition: the condition to add.
        """
        current_expressions = [
            cond.to_pddl()
            for _, cond in self.__iter__()
            if isinstance(cond, NumericalExpressionTree)
        ]
        if condition.to_pddl() not in current_expressions:
            self.operands.add(condition)

    @staticmethod
    def _simplify_numeric_preconditions(
        numeric_preconditions: List[NumericalExpressionTree],
        decimal_digits: int = DEFAULT_DECIMAL_DIGITS,
    ) -> List[str]:
        """Simplify the numeric preconditions by eliminating redundant conditions as well as removing redundant preconditions.

        :param numeric_preconditions: the numeric preconditions to simplify.
        :param decimal_digits: the number of decimal digits to keep.
        :return: the simplified numeric preconditions.
        """
        # start by searching for the equality conditions that can be used to eliminate some variables in the other conditions
        new_expressions = [
            precondition.__copy__() for precondition in numeric_preconditions
        ]
        equality_conditions = [
            condition for condition in new_expressions if condition.root.value == "="
        ]

        assumptions = []
        for equality_condition in equality_conditions:
            eliminated_expression = equality_condition.extract_eliminated_expressions()
            if eliminated_expression is None:
                continue

            expression_to_eliminate, replacing_expression = eliminated_expression
            assumptions.append(
                f"{expression_to_eliminate.to_mathematical()} = {replacing_expression.to_mathematical()}"
            )

        simplified_conditions = []
        for condition in new_expressions:
            if condition.root.value == "=":
                simplified_equation = simplify_equality(
                    condition.to_mathematical()[1:-1]
                )
                if simplified_equation:
                    simplified_conditions.append(simplified_equation)

                continue

            simplified_inequality = simplify_inequality(
                condition.to_mathematical(),
                condition.root.value,
                [assumption for assumption in assumptions],
                decimal_digits=decimal_digits,
            )
            if simplified_inequality:
                simplified_conditions.append(simplified_inequality)

        return simplified_conditions

    def add_condition(
        self,
        condition: Union[
            "Precondition", Predicate, GroundedPredicate, NumericalExpressionTree
        ],
        check_duplications: bool = False,
    ) -> None:
        """Add a condition to the precondition.

        :param condition: the condition to add.
        :param check_duplications: whether to check for duplications.
        """
        if isinstance(condition, (Predicate, GroundedPredicate)):
            if not check_duplications:
                self.operands.add(condition)

            else:
                self._unique_add_predicate(condition)

        elif isinstance(condition, NumericalExpressionTree):
            if not check_duplications:
                self.operands.add(condition)

            else:
                self._unique_add_numeric_expression(condition)

        else:
            current_compound_conditions = [
                str(cond)
                for _, cond in self.__iter__()
                if isinstance(cond, Precondition)
            ]
            if str(condition) not in current_compound_conditions:
                self.operands.add(condition)

    @staticmethod
    def _remove_condition(
        condition_to_remove: Union[
            "Precondition", Predicate, GroundedPredicate, NumericalExpressionTree
        ],
        searched_condition: "Precondition",
    ) -> bool:
        """Tries to remove the input precondition from the searched precondition.

        :param condition_to_remove: the condition to remove.
        :param searched_condition: the precondition to search in.
        :return: True if the condition was removed, False otherwise.
        """
        for operand in searched_condition.operands:
            if (
                isinstance(operand, type(condition_to_remove))
                and operand == condition_to_remove
            ):
                searched_condition.operands.remove(operand)
                return True

            elif isinstance(operand, Precondition):
                if Precondition._remove_condition(condition_to_remove, operand):
                    return True

        return False

    def remove_condition(
        self,
        condition: Union[
            "Precondition", Predicate, GroundedPredicate, NumericalExpressionTree
        ],
    ) -> bool:
        """Remove a condition from the precondition.

        :param condition: the condition to remove.
        :return: True if the condition was removed, False otherwise.
        """
        return self._remove_condition(condition, self)

    def add_equality_condition(
        self, condition: Tuple[str, str], inequality: bool = False
    ) -> None:
        """Add an equality condition to the precondition.

        :param condition: the equality condition to add
        :param inequality: whether the condition is an inequality
        """
        if not inequality:
            self.equality_preconditions.add(condition)
        else:
            self.inequality_preconditions.add(condition)

    def change_signature(self, old_to_new_param_names: Dict[str, str]) -> None:
        """Change the signature of the compound precondition.

        :param old_to_new_param_names:
        :return:
        """
        for _, condition in self:
            if isinstance(condition, Predicate):
                condition.change_signature(old_to_new_param_names)

            elif isinstance(condition, NumericalExpressionTree):
                condition.change_signature(old_to_new_param_names)

            elif isinstance(condition, Precondition):
                condition.change_signature(old_to_new_param_names)

        new_equality_conditions = set()
        new_inequality_conditions = set()
        for equality_condition in self.equality_preconditions:
            param_1, param_2 = equality_condition
            new_equality_conditions.add(
                (old_to_new_param_names[param_1], old_to_new_param_names[param_2])
            )

        self.equality_preconditions = new_equality_conditions
        for inequality_condition in self.inequality_preconditions:
            param_1, param_2 = inequality_condition
            new_inequality_conditions.add(
                (old_to_new_param_names[param_1], old_to_new_param_names[param_2])
            )

        self.inequality_preconditions = new_inequality_conditions


class UniversalPrecondition(Precondition):
    """Class representing a universally quantified precondition."""

    quantified_parameter: str
    quantified_type: PDDLType

    def __init__(
        self,
        quantified_parameter: str,
        quantified_type: PDDLType,
        binary_operator: str = "and",
    ):
        self.quantified_parameter = quantified_parameter
        self.quantified_type = quantified_type
        super().__init__(binary_operator)

    def __str__(self):
        if len(self.operands) == 0:
            return ""

        internal_condition_string = super()._print_self()
        return (
            f"(forall ({self.quantified_parameter} - {self.quantified_type.name})"
            f"\n\t{internal_condition_string})"
        )

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: "UniversalPrecondition") -> bool:
        return (
            super().__eq__(other)
            and self.quantified_parameter == other.quantified_parameter
            and self.quantified_type == other.quantified_type
        )


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

    def add_condition(
        self,
        condition: Union[
            Precondition,
            UniversalPrecondition,
            Predicate,
            GroundedPredicate,
            NumericalExpressionTree,
        ],
    ) -> None:
        """Add a condition to the compound precondition.

        :param condition: the condition to add.
        """
        self.root.add_condition(condition)

    def remove_condition(
        self,
        condition: Union[
            Precondition,
            UniversalPrecondition,
            Predicate,
            GroundedPredicate,
            NumericalExpressionTree,
        ],
    ) -> None:
        """Remove a condition from the compound precondition.

        :param condition: the condition to remove.
        """
        self.root.remove_condition(condition)

    def change_signature(self, old_to_new_param_names: Dict[str, str]) -> None:
        """Change the signature of the compound precondition.

        :param old_to_new_param_names:
        """
        self.root.change_signature(old_to_new_param_names)

    def print(self, decimal_digits: int = DEFAULT_DECIMAL_DIGITS) -> str:
        """Print the compound precondition in PDDL format.

        Note:
            This code is used for legacy support for the new NSAM paper and will be deleted in future versions.

        :param decimal_digits: the number of decimal digits to keep.
        """
        return self.root.print(decimal_digits)
