from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser


class EndStatementParser(AbcStatementParser):

    def __init__(self, parser):
        super().__init__(parser)
        self.statement = Statement()

    def accept(self):

        if self.parser.index <= len(self.parser.body) - 1:
            if self.token().type == TokenType.Comma:
                if self.ternary_end():
                    self.parser.statement.add(self.token())
                    self.move()
                    return True
                else: self.parser.statement.add(self.token())
            elif self.token().type == TokenType.Rp:
                # if self.ternary_end():
                #     self.move()
                #     return True
                self.move()
                return True
        else:
            if self.ternary_end():
                return True
        return False

    def ternary_end(self):
        if self.parser.ternary_stack.count() > 0 and self.parser.ternary_stack.top().type == TokenType.Colon and self.parser.ternary_stack.top(
                -1).type == TokenType.Question:
            i = self.parser.statement.count() - 1
            while i > 0:
                if self.parser.statement.body[i].type == TokenType.Colon:
                    for j in range(i + 1, self.parser.statement.count()):
                        self.statement.add(self.parser.statement.body[j])
                    self.parser.statement.remove(i)
                    self.parser.statement.add(self.statement)
                    break
                i -= 1
            if self.parser.index <= len(self.parser.body) - 1:
                self.statement.add(self.token())
            self.parser.ternary_stack.clear()
            return True
        return False
