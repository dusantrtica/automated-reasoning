from src.model.simplify import simplify, nnf
from src.model.satisfy import atoms_count
from src.model.valuation import valuation
import pytest
import sys
from src.model.formula import *

def test_to_string():
     # (p0 and p1) => ~p2
    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)
    formula = Impl(left_formula, right_formula)

    s = to_string(formula)

    assert s == "((0/\\1)=>~2)"

def test_complexit():
      # (p0 and p1) => ~p2
    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)
    formula = Impl(left_formula, right_formula)

    # act
    formula_complexity = complexity(formula)

    # assert
    assert formula_complexity == 3

def test_formula_equality():
    # Arrange
    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)
    formula1 = Impl(left_formula, right_formula)

    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)
    formula2 = Impl(left_formula, right_formula)

    assert formula1 == formula2

def test_evaluation():
     # Arrange p0 and p1 => not p2
    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)


    formula = Impl(left_formula, right_formula)

    assert formula.evaluate([0, 0, 0]) == True
    assert formula.evaluate([1, 1, 1]) == False


def test_valuation():
    gen = valuation(3)

    assert next(gen) == [False, False, False]
    assert next(gen) == [False, False, True]
    assert next(gen) == [False, True, False]
    assert next(gen) == [False, True, True]
    assert next(gen) == [True, False, False]
    assert next(gen) == [True, False, True]
    assert next(gen) == [True, True, False]
    assert next(gen) == [True, True, True]


def test_atoms_count_formula_with_atmos():
    # Arrange p0 and p1 => not p2
    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)


    formula = Impl(left_formula, right_formula)

    assert atoms_count(formula) == 3

def test_atmos_count_formula_without_atoms():
     # Arrange p0 and p1 => not p2
    p0: Formula = Truthy()
    p1: Formula = Falsy()
    p2: Formula = Truthy()

    left_formula = And(p0, p1)
    right_formula = Not(p2)


    formula = Impl(left_formula, right_formula)
    assert atoms_count(formula) == 0

def test_simplify_formula_with_implication():
    # Arrange
    # (T and Po) => (T or P1)
    formula = Impl(And(Truthy(), Atom(0)), Or(Truthy(), Atom(1)))

    # Act
    simplified = simplify(formula)

    # Assert
    assert simplified == Truthy()

def test_simplify_formula_with_implication_with_atoms():
    # Arrange
    # (T and Po) => (T or P1)
    formula = Impl(And(Truthy(), Atom(0)), Or(Falsy(), Atom(1)))

    # Act
    simplified = simplify(formula)

    # Assert simplified = P0 => P1
    assert simplified == Impl(Atom(0), Atom(1))

def test_nnf_with_implication():
    # Arrange: formula = p0 => p1
    formula = Impl(Atom(0), Atom(1))

    # Act
    nnf_formula = nnf(formula)

    # Assert nnf_formula == ~p0 | p1
    assert nnf_formula == Or(Not(Atom(0)), Atom(1))

def test_nnf_with_implication_and_negation_in_front():
    # Arrange: formula = p0 => p1
    formula = Not(Impl(Atom(0), Atom(1)))

    # Act
    nnf_formula = nnf(formula)

    # Assert nnf_formula == ~p0 | p1
    assert nnf_formula == And(Atom(0), Not(Atom(1)))

def test_nnf_with_implication_and_double_negation_in_front():
    # Arrange: formula = p0 => p1
    formula = Not(Not(Impl(Atom(0), Atom(1))))

    # Act
    nnf_formula = nnf(formula)

    # Assert nnf_formula == ~p0 | p1
    assert nnf_formula == Or(Not(Atom(0)), Atom(1))


if __name__ == '__main__':
    sys.exit(pytest.main())