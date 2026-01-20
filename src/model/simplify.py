from doctest import FAIL_FAST
from src.model.formula import And, BinaryData, Eql, Falsy, Formula, Impl, Not, Or, Truthy, Type

def simplify_not(formula: Formula) -> Formula:
    sub_formula = simplify(formula.data)
    
    # 3 cases
    if sub_formula.formula_type == Type.TRUE:
        return Falsy()
    if sub_formula.formula_type == Type.FALSE:
        return Truthy()

    return Not(sub_formula)

def simplify_and(formula: Formula) -> Formula:
    """
    x and y, we recursievely simplify left and right parts of it
    if, after simplification, x is True (constant), we return right part of formula
    as True AND P = P
    """
    left_simplified = simplify(formula.data.left)
    right_simplified = simplify(formula.data.right)

    if left_simplified.formula_type == Type.TRUE:
        return right_simplified
    if right_simplified.formula_type == Type.TRUE:
        return left_simplified
    
    if left_simplified == Type.FALSE or right_simplified == Type.FALSE:
        return Falsy()

    return And(left_simplified, right_simplified)

def simplify_or(formula: Formula) -> Formula:
    left_simplified = simplify(formula.data.left)
    right_simplified = simplify(formula.data.right)

    if left_simplified.formula_type == Type.TRUE or right_simplified.formula_type == Type.TRUE:
        return Truthy()
    
    if left_simplified.formula_type == Type.FALSE:
        return right_simplified
    if right_simplified.formula_type == Type.FALSE:
        return left_simplified

    return Or(left_simplified, right_simplified)

def simplify_impl(formula: Formula) -> Formula:
    left_simplified = simplify(formula.data.left)
    right_simplified = simplify(formula.data.right)

    """
    Trivial cases: F => P == T and P => T == T
    Non Trivial cases: T => P == P and P => F == Not(P)
    """
    if left_simplified.formula_type ==  Type.FALSE or right_simplified.formula_type == Type.TRUE:
        return Truthy()

    if left_simplified.formula_type == Type.TRUE:
        return right_simplified
    
    if right_simplified.formula_type == Type.FALSE:
        return simplify(Not(left_simplified))

    return Impl(left_simplified, right_simplified)

def simplify_eql(formula: Formula) -> Formula:
    left_simplified = simplify(formula.data.left)
    right_simplified = simplify(formula.data.right)
    

    if left_simplified.formula_type == Type.TRUE:
        return right_simplified
    if right_simplified.formula_type == Type.TRUE:
        return left_simplified

    if left_simplified.formula_type == Type.FALSE:
        return simplify(Not(right_simplified))

    if right_simplified.formula_type == Type.FALSE:
        return simplify(Not(left_simplified))

    return Eql(left_simplified, right_simplified)

# Get rid of constants p0 and True = p0
def simplify(formula: Formula) -> Formula:
    match formula.formula_type:
        case Type.TRUE | Type.FALSE | Type.ATOM:
            return formula
        case Type.NOT:
            return simplify_not(formula.data)
        case Type.BINARY:
            match formula.data.binary_type:
                case BinaryData.Type.AND:
                    return simplify_and(formula)
                case BinaryData.Type.OR:
                    return simplify_or(formula)
                case BinaryData.Type.EQL:
                    return simplify_eql(formula)
                case BinaryData.Type.IMPL:
                    return simplify_impl(formula)
