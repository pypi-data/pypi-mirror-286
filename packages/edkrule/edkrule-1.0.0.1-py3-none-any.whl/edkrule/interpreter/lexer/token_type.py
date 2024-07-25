import enum


class TokenType(enum.Enum):
    Expression = 1000
    Statement = 1001
    Initial = 0
    Identifier = 1
    Assignment = 2
    Eq = 3
    NEq = 4
    Lt = 5
    Le = 6
    Gt = 7
    Ge = 8
    Variable = 9
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
    TRUE = 22
    FALSE = 23
    Blank = 24
    DPlus = 25
    PlusEq = 26
    DMinus = 27
    MinusEq = 28
    Comma = 29
    Question = 30
    Ep = 31
    Nidentity = 32
    AwaysEq = 33
    EqPlus = 34
    EqMinus = 35
    Divide = 36
    Multipy = 37
    Dot = 38
