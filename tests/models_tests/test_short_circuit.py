from unittest.mock import MagicMock

from pddl_plus_parser.models.grounded_precondition import GroundedPrecondition
from pddl_plus_parser.models.pddl_precondition import Precondition, CompoundPrecondition
from pddl_plus_parser.models.pddl_predicate import GroundedPredicate


def test_and_or_combination_short_circuit():
    domain = MagicMock()
    action = MagicMock()

    pred_true = GroundedPredicate(name="p1", signature={}, object_mapping={})
    pred_should_not_run = GroundedPredicate(name="p2", signature={}, object_mapping={})
    pred_after_or = GroundedPredicate(name="p3", signature={}, object_mapping={})

    inner_or = Precondition("or")
    inner_or.add_condition(pred_true)
    inner_or.add_condition(pred_should_not_run)

    outer_and = Precondition("and")
    outer_and.add_condition(inner_or)
    outer_and.add_condition(pred_after_or)

    compound = CompoundPrecondition()
    compound.root = outer_and

    gp = GroundedPrecondition(compound, domain, action)
    gp._grounded_precondition = compound

    state = MagicMock()
    state.serialize.return_value = {pred_true.untyped_representation}

    res = gp.is_applicable(state)

    assert res is False


def test_or_and_combination_short_circuit():
    domain = MagicMock()
    action = MagicMock()

    pred_false = GroundedPredicate(name="p1", signature={}, object_mapping={})
    pred_should_not_run = GroundedPredicate(name="p2", signature={}, object_mapping={})
    pred_true = GroundedPredicate(name="p3", signature={}, object_mapping={})

    inner_and = Precondition("and")
    inner_and.add_condition(pred_false)
    inner_and.add_condition(pred_should_not_run)

    outer_or = Precondition("or")
    outer_or.add_condition(inner_and)
    outer_or.add_condition(pred_true)

    compound = CompoundPrecondition()
    compound.root = outer_or

    gp = GroundedPrecondition(compound, domain, action)
    gp._grounded_precondition = compound

    state = MagicMock()
    state.serialize.return_value = {pred_true.untyped_representation}

    res = gp.is_applicable(state)

    assert res is True


def test_nested_and_or_short_circuit():
    domain = MagicMock()
    action = MagicMock()

    pred_true = GroundedPredicate(name="p1", signature={}, object_mapping={})
    pred_unused = GroundedPredicate(name="p2", signature={}, object_mapping={})
    pred_false = GroundedPredicate(name="p3", signature={}, object_mapping={})

    inner_or = Precondition("or")
    inner_or.add_condition(pred_true)
    inner_or.add_condition(pred_unused)

    outer_and = Precondition("and")
    outer_and.add_condition(inner_or)
    outer_and.add_condition(pred_false)

    compound = CompoundPrecondition()
    compound.root = outer_and

    gp = GroundedPrecondition(compound, domain, action)
    gp._grounded_precondition = compound

    state = MagicMock()
    state.serialize.return_value = {pred_true.untyped_representation}

    res = gp.is_applicable(state)

    assert res is False
