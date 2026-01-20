from src.model.formula import Formula, Type
from src.model.valuation import valuation

def atoms_count(formula: Formula) -> int:
    match formula.formula_type:
        case Type.TRUE | Type.FALSE:
            return 0
        case Type.ATOM:
            return 1
        case Type.NOT:
            return atoms_count(formula.data)
        case Type.BINARY:
            return atoms_count(formula.data.left) + atoms_count(formula.data.right)

def satisfiable_valuation(formula: Formula) -> list[bool] | None:
    num_of_atoms = atoms_count(formula)
    for val in valuation(num_of_atoms):
        if formula.evaluate(val):
            return val
    return None

def is_falsifiable(formula: Formula) -> bool:
    pass

def is_equivalent(formula1: Formula, formula2: Formula) -> bool:
    f1_num_atoms = atoms_count(formula1)
    f2_num_atoms = atoms_count(formula2)

    if f1_num_atoms != f2_num_atoms:
        return False

    for val in valuation(f1_num_atoms):
        if formula1.evaluate(val) != formula2.evaluate(val):
            return False

    return True

def is_consequence(f: Formula, g: Formula):
    pass