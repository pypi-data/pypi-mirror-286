from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser


class QuestionStatementParser(AbcStatementParser):

    def __init__(self, parser):
        super().__init__(parser)
        self.statement = Statement()

    def accept(self):
        if self.parser.index <= len(self.parser.body) - 1:
            if self.token().type == TokenType.Question:
                self.parser.ternary_stack.push(self.token())
                self.parser.statement.add(self.token())
                self.move()
                return True
            # self.move()
        return False
