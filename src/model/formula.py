from enum import Enum, auto

class Type(Enum):
    FALSE=auto()
    TRUE=auto()
    ATOM=auto()
    NOT=auto()
    BINARY=auto()

    # AND=auto()
    # OR=auto()
    # IMPL=auto()
    # EQL=auto()


class Formula:
    # type of node
    # T, F, implication, conjuntction, atom....
    # pointers to left and right sub formula
    formula_type: Type
    data = None

    def __eq__(self, value: object, /) -> bool:
        if self.formula_type != value.formula_type:
            return False
        match self.formula_type:
            case Type.TRUE | Type.FALSE:
                return True
            case Type.ATOM | Type.NOT:
                return self.data == value.data
            case Type.BINARY:
                if self.data.binary_type != value.data.binary_type:
                    return False
                return self.data.left == value.data.left and self.data.right == value.data.right

    def evaluate(self, valuation: list[int]) -> bool:
        match self.formula_type:
            case Type.FALSE:
                return False
            case Type.TRUE:
                return True
            case Type.ATOM:
                return valuation[self.data]
            case Type.NOT:
                return not self.data.evaluate(valuation)
            case Type.BINARY:
                return self.data.evaluate(valuation)

    
class AtomData:
    def __init__(self) -> None:
        self.n = 0
    
class NotData:
    def __init__(self) -> None:
        self.formula = None

class FalseData:
    pass

class TrueData:
    pass

class BinaryData:
    def __init__(self, l, r) -> None:
        self.left = l
        self.right = r

    class Type(Enum):
        AND=auto()
        OR=auto()
        IMPL=auto()
        EQL=auto()
        
        def __str__(self) -> str:
            name = self.name
            match name:
                case 'AND':
                    return "/\\"
                case 'OR':
                    return "||"
                case 'IMPL':
                    return "=>"
                case 'EQL':
                    return "<=>"
                case _:
                    return ""

    
    binary_type: Type = None
    left: Formula = None
    right: Formula = None

    def evaluate(self, valuation: list[int]) -> bool:
        left_value = self.left.evaluate(valuation)
        right_value = self.right.evaluate(valuation)
        if self.binary_type == BinaryData.Type.AND:
            return left_value and right_value
        elif self.binary_type == BinaryData.Type.OR:
            return left_value or right_value
        elif self.binary_type == BinaryData.Type.EQL:
            return left_value == right_value
        elif self.binary_type == BinaryData.Type.IMPL:
            return not left_value or right_value


def Not(formula: Formula) -> Formula:
    not_formula = Formula()
    not_formula.formula_type = Type.NOT
    not_formula.data = formula
    return not_formula

def Falsy() -> Formula:
    false_formula = Formula()
    false_formula.formula_type = Type.FALSE
    return false_formula

def Truthy() -> Formula:
    true_formula = Formula()
    true_formula.formula_type = Type.TRUE
    return true_formula

def Atom(n) -> Formula:
    atom_formula = Formula()
    atom_formula.formula_type = Type.ATOM
    atom_formula.data = n
    return atom_formula

def _binary_formula(l: Formula, r: Formula) -> Formula:
    bin_formula = Formula()
    bin_formula.formula_type = Type.BINARY
    bin_formula.data = BinaryData(l, r)
    return bin_formula

def And(l: Formula, r: Formula) -> Formula:
    and_formula = _binary_formula(l, r)
    and_formula.data.binary_type = BinaryData.Type.AND
    return and_formula

def Or(l: Formula, r: Formula) -> Formula:
    or_formula = _binary_formula(l, r)
    or_formula.data.binary_type = BinaryData.Type.OR
    return or_formula

def Eql(l: Formula, r: Formula) -> Formula:
    eq_formula = _binary_formula(l, r)
    eq_formula.data.binary_type = BinaryData.Type.EQL
    return eq_formula

def Impl(l: Formula, r: Formula) -> Formula:
    impl_formula = _binary_formula(l, r)
    impl_formula.data.binary_type = BinaryData.Type.IMPL
    return impl_formula

def to_string(formula: Formula) -> str:
    formula_type = formula.formula_type
    match formula_type:
        case Type.FALSE:
            return "F"
        case Type.TRUE:
            return "T"
        case Type.ATOM:
            return str(formula.data)
        case Type.NOT:
            return "~" + to_string(formula.data)
        case Type.BINARY:
            return "(" + to_string(formula.data.left) + str(formula.data.binary_type) + to_string(formula.data.right) + ")" 
        case _:
            return ""

def complexity(formula: Formula) -> int:
    match formula.formula_type:
        case Type.ATOM | Type.FALSE | Type.ATOM:
            return 0
        case Type.NOT:
            return 1 + complexity(formula.data)
        case Type.BINARY:
            return 1 + complexity(formula.data.left) + complexity(formula.data.right)

def substitute(formula: Formula, what_to_substitute: Formula, substitute_with: Formula):
    if formula == what_to_substitute:
        return substitute_with
    
    match formula.formula_type:
        case Type.TRUE | Type.FALSE | Type.ATOM:
            return formula
        case Type.NOT:
            return Not(substitute(formula.data, what_to_substitute, substitute_with))
        case Type.BINARY:
            left_substituted = substitute(formula.data.left, what_to_substitute, substitute_with)
            right_substituted = substitute(formula.data.right, what_to_substitute, substitute_with)
            bin_formula = _binary_formula(left_substituted, right_substituted)
            bin_formula.data.binary_type = formula.data.binary_type
            return bin_formula
        

if __name__ == '__main__':
    # (p0 and p1) => ~p2
    p0: Formula = Atom(0)
    p1: Formula = Atom(1)
    p2: Formula = Atom(2)

    left_formula = And(p0, p1)
    right_formula = Not(p2)
    formula = Impl(left_formula, right_formula)
