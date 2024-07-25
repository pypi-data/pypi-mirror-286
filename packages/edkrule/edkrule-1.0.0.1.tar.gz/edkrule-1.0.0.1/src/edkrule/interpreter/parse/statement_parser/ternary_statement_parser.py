from edkrule.interpreter.expression.stack import Stack
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser
from edkrule.interpreter.parse.ternary_stack import TernaryStack


class TernaryStatementParser(AbcStatementParser):
    def __init__(self, parser):
        super().__init__(parser)
        self.left_statement = Statement()
        self.right_statement = Statement()
        self.left_flag = TernaryStack()
        self.right_flag = TernaryStack()
        self.left_content = []
        self.right_content = []
        self.bracket_stack = Stack()

    def accept(self) -> bool:

        if self.parser.index <= len(self.parser.body) - 1:
            if self.token().type == TokenType.Question:
                self.parser.statement.add(self.token())
                self.left_flag.append(self.token())
                self.left()
                self.right()
                return True
            # self.move()
        return False

    def ternary_end(self):
        if self.parser.index > len(self.parser.body) - 1:
            return True
        if self.token().type == TokenType.Comma:
            if self.bracket_stack.empty():
                return True
        if self.token().type == TokenType.Rp:
            if self.bracket_stack.empty():
                return True
        return False
        # return self.parser.index > len(
        #     self.parser.content) - 1 or self.token().type == TokenType.Comma or self.token().type == TokenType.Rp

    def left(self):
        from edkrule.interpreter.parse.parser import Parser
        while not self.left_flag.empty():
            self.move()

            if self.token().type == TokenType.Question:
                self.left_flag.append(self.token())
                self.left_content.append(self.token())
            elif self.token().type == TokenType.Colon:
                self.left_flag.pop()
                if not self.left_flag.empty(): self.left_content.append(self.token())
            else:
                self.left_content.append(self.token())
        parser = Parser(self.left_content).parse()
        self.left_statement = parser.statement
        self.right_flag.append(self.token())
        self.parser.statement.add(self.left_statement)
        self.parser.statement.add(self.token())

    def right(self):
        from edkrule.interpreter.parse.parser import Parser
        while not self.right_flag.empty():
            self.move()
            if self.parser.index <= len(self.parser.body) - 1:
                if self.token().type == TokenType.Lp:
                    self.bracket_stack.push(self.token())
                if self.token().type == TokenType.Rp:
                    self.bracket_stack.pop()
            # self.right_content.append(self.token())
            if self.ternary_end():
                if self.parser.index <= len(self.parser.body) - 1:
                    if self.token().type == TokenType.Rp:
                        self.right_content.append(self.token())
                self.right_flag.pop()
                parser = Parser(self.right_content).parse()
                self.right_statement = parser.statement
                # self.right_flag.append(self.token())
                self.parser.statement.add(self.right_statement)
            else:
                self.right_content.append(self.token())
