from src.model.formula import BinaryData, Formula, Type


class Literal:
    def __init__(self, positive, atom_value):
        self.positive = positive
        self.atom = atom_value


Clause = list[Literal]
NormalForm = list[Clause]

def concat(left: NormalForm, right: NormalForm) -> NormalForm:    
    return [*left, *right]

def concat_clause(c1: Clause, c2: Clause) -> Clause:
    return [*c1, *c2]

def cross(left: NormalForm, right: NormalForm) -> NormalForm:
    result: NormalForm = []
    for c1 in left:
        for c2 in right:
            result.append(concat_clause(c1, c2))

def cnf (formula: Formula) -> NormalForm:
    match formula.formula_type:
        case Type.TRUE:
            return []
        case Type.FALSE:
            return [[]]
        case Type.ATOM:
            return [[Literal(True, formula.data)]]
        case Type.NOT:
            return [[Literal(False, formula.data)]]
        case Type.BINARY:
            match formula.data.binary_type:
                case BinaryData.AND:
                    return concat(cnf(formula.data.left), cnf(formula.data.right))
                case BinaryData.OR:
                    return cross(cnf(formula.data.left), cnf(formula.data.right))
                