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
                

class AtomWrapper:
    def __init__(self, value):
        self.n = value

    def return_and_increment(self):
        self.n += 1
        return self.n-1



def tseitin_substitution(formula: Formula, normal_form: NormalForm, atom_wrapper: AtomWrapper) -> int:
    match formula.formula_type:
        case Type.ATOM:
            return formula.data
        case Type.TRUE:
            normal_form.append([Literal(True, atom_wrapper.n)])
            return atom_wrapper.return_and_increment()
        case Type.FALSE:
            normal_form.append([Literal(False, atom_wrapper.n)])
            return atom_wrapper.return_and_increment()
        case Type.NOT:
            sub_formula = tseitin_substitution(formula.data, normal_form, atom_wrapper)
            tseitin_not = [
                [Literal(False, sub_formula), Literal(False, atom_wrapper.n)],
                [Literal(True, sub_formula), Literal(True, atom_wrapper.n)]]
            normal_form.append(tseitin_not)

            return atom_wrapper.return_and_increment()

        case Type.BINARY:                            # left and right are substitution letters, integers
            left = tseitin_substitution(formula.data.left, normal_form, atom_wrapper)
            right = tseitin_substitution(formula.data.right, normal_form, atom_wrapper)
            match formula.data.binary_type:
                case BinaryData.Type.AND:
                    tseitin_binary = [
                        [Literal(False, atom_wrapper.n), Literal(True, left)],
                        [Literal(False, atom_wrapper.n), Literal(True, right)],
                        [Literal(True, atom_wrapper.n), Literal(False, left), Literal(False, right)]
                    ]
                    normal_form.append(*tseitin_binary)
                    return atom_wrapper.return_and_increment()

                    
def tseitin(formula: Formula) -> NormalForm:
    normal_form = []
    atom_count = atom_count(formula)
    atom_wrapper = AtomWrapper(atom_count+1)
    s = tseitin_substitution(formula, normal_form, atom_wrapper)
    normal_form.append([Literal(True, s)])
    return normal_form
