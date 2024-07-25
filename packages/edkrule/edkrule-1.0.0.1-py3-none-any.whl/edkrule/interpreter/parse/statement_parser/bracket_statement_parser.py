from edkrule.interpreter.lexer.token_type import TokenType
# from edkrule.tests.interpreter.interpreter import Stack

from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser
from edkrule.utils.stack import Stack


# from pybiz.tests.interpreter.parse.parser import Parser


class BracketStatementParser(AbcStatementParser):

    def __init__(self, parser):
        super().__init__(parser)
        self.bracket_stack = Stack()
        self.statement = Statement()
        self.body_content = []

    def accept(self):
        if self.parser.index <= len(self.parser.body) - 1:
            if self.token().type == TokenType.Lp:
                # 括号入栈
                self.bracket_stack.push(self.token())
                # 添加左括号节点
                self.statement.add(self.token())
                # 方法体的读取
                while self.bracket_stack.count() != 0:
                    self.move()
                    # 新的左括号入栈，右括号出栈，保证方法体能读取完
                    if self.token().type == TokenType.Rp:
                        self.bracket_stack.pop()
                    elif self.token().type == TokenType.Lp:
                        self.bracket_stack.push(self.token())
                    # 判断是否是方法体结束的右括号
                    # 否: 则加入body_content，以便读取完后再次解析
                    if not self.bracket_stack.count() == 0:
                        self.body_content.append(self.token())
                from edkrule.interpreter.parse.parser import Parser
                parser = Parser(self.body_content).parse()

                self.statement.add(parser.statement)
                self.statement.add(self.token())
                self.move()
                if not self.statement.empty():
                    self.parser.statement.add(self.statement)
                return True
        return False
