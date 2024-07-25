
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser


class NormalStatementParser(AbcStatementParser):

    def __init__(self, parser):
        super().__init__(parser)
        self.statement = Statement()

    def accept(self):
        if self.parser.index <= len(self.parser.body) - 1:
            if self.token().type == TokenType.Identifier and self.parser.index < len(
                    self.parser.body) - 1 and self.token(offset=1).type == TokenType.Lp:
                # FunctionStatement 改函数跳出循环
                return False
            if self.token().type in [TokenType.Plus, TokenType.Comma, TokenType.Eq,
                                     TokenType.Minus, TokenType.DPlus, TokenType.DMinus,
                                     TokenType.Multipy, TokenType.Divide,
                                     TokenType.And, TokenType.Or, TokenType.Eq,
                                     TokenType.Ep, TokenType.NEq, TokenType.Nidentity,
                                     TokenType.EqPlus, TokenType.MinusEq, TokenType.EqMinus,
                                     TokenType.PlusEq, TokenType.Assignment
                                     ]:
                self.parser.statement.add(self.token())
            elif self.token().type in [TokenType.Question, TokenType.Colon, TokenType.Lp, TokenType.Rp]:
                return False
            else:
                self.statement.add(self.token())
                self.parser.statement.add(self.statement)
            self.move()
        return True
