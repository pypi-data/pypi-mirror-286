import enum


@enum.unique
class DfaState(enum.Enum):
    Initial = 0
    Identifier = 1
    Assignment = 2
    Eq = 3
    NEq = 4
    Lt = 5
    Le = 6
    Gt = 7
    Ge = 8
    Var = 9
    Lp = 10
    Rp = 11
    Dq = 12
    Sq = 13
    Colon = 14
    Plus = 15
    Minus = 16
    RealNumber = 17
    ByteAnd = 18
    And = 19
    ByteOr = 20
    Or = 21
    True1 = 22
    True2 = 23
    True3 = 24
    True4 = 25
    False1 = 26
    False2 = 27
    False3 = 28
    False4 = 29
    False5 = 30
    Blank = 31
    DPlus = 32
    PlusEq = 33
    DMinus = 34
    MinusEq = 35
    Comma = 36
    Question = 37
    Ep = 38
    Nidentity = 39
    AwaysEq = 40
    EqMinus = 41
    EqPlus = 42
    Divide = 43
    Multipy = 44
    Dot = 45




