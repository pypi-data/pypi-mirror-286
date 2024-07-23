from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.token import Token


class Priority:
    @staticmethod
    def level(token: Token):
        if token.type in [TokenType.Plus, TokenType.Minus, TokenType.DPlus, TokenType.DMinus]: return 1
        if token.type in [TokenType.Multipy, TokenType.Divide]: return 2
        if token.type in [TokenType.And, TokenType.Or, TokenType.Eq,
                          TokenType.Ep, TokenType.NEq, TokenType.Nidentity,
                          TokenType.EqPlus, TokenType.MinusEq, TokenType.EqMinus,
                          TokenType.PlusEq, TokenType.Gt, TokenType.Ge, TokenType.Lt, TokenType.Le]: return 0
        if token.type in [TokenType.Colon, TokenType.Question]: return -1
        if token.type in [TokenType.Assignment]: return -2

    @staticmethod
    def compare(token: Token, with_token: Token):
        if Priority.level(token) > Priority.level(with_token):
            return 1
        elif Priority.level(token) == Priority.level(with_token):
            return 0
        else:
            return -1

    @staticmethod
    def gt(token: Token, with_token: Token):
        return Priority.compare(token, with_token) == 1

    @staticmethod
    def lt(token: Token, with_token: Token):
        return Priority.compare(token, with_token) == -1

    @staticmethod
    def eq(token: Token, with_token: Token):
        return Priority.compare(token, with_token) == 0