from edkrule.interpreter.lexer.token_type import TokenType


class Categorize:
    @staticmethod
    def is_op(stmt):
        return stmt.type in [TokenType.Plus, TokenType.Minus, TokenType.DPlus, TokenType.DMinus,
                             TokenType.Multipy, TokenType.Divide, TokenType.And, TokenType.Or,
                             TokenType.Eq, TokenType.Ep, TokenType.NEq, TokenType.Nidentity,
                             TokenType.EqPlus, TokenType.MinusEq, TokenType.EqMinus, TokenType.PlusEq,
                             TokenType.Assignment, TokenType.Colon, TokenType.Question,
                             TokenType.Gt, TokenType.Ge, TokenType.Le, TokenType.Lt]

    @staticmethod
    def is_variable(stmt):
        return stmt.type in [TokenType.Identifier, TokenType.Lp,
                             TokenType.RealNumber, TokenType.TRUE,
                             TokenType.FALSE, TokenType.Variable]

    @staticmethod
    def is_exp(stmt):
        return stmt.type in [TokenType.Identifier, TokenType.Lp,
                             TokenType.RealNumber, TokenType.TRUE,
                             TokenType.FALSE, TokenType.Expression,
                             TokenType.Variable]

    @staticmethod
    def is_stmt(stmt):
        return stmt.type == TokenType.Statement