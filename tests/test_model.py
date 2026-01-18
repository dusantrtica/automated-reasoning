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
    assert formula.evaluate([1, 0, 1]) == False


if __name__ == '__main__':
    sys.exit(pytest.main())