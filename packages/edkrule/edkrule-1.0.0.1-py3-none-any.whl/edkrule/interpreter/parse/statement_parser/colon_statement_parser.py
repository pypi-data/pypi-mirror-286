from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser


class ColonStatementParser(AbcStatementParser):

    def __init__(self, parser):
        super().__init__(parser)
        self.statement = Statement()

    def accept(self):
        if self.parser.index <= len(self.parser.body) - 1:
            if self.token().type == TokenType.Colon:
                if not self.parser.ternary_stack.empty() and self.parser.ternary_stack.top().type == TokenType.Question:
                    i = self.parser.statement.count()-1
                    while i > 0:
                        if self.parser.statement.body[i].type == TokenType.Question:
                            for j in range(i+1, self.parser.statement.count()):
                                self.statement.add(self.parser.statement.body[j])
                            self.parser.statement.remove(i)
                            self.parser.statement.add(self.statement)
                            break
                        i -= 1
                    self.parser.ternary_stack.push(self.token())
                self.parser.statement.add(self.token())
                self.move()
                return True
        return False
