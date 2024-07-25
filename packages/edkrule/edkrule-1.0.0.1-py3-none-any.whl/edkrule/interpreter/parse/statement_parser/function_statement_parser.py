from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.token import Token
# from edkrule.tests.interpreter.interpreter import Stack

from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.base_statement_parser import AbcStatementParser
from edkrule.utils.stack import Stack


# from pybiz.tests.interpreter.parse.parser import Parser


class FunctionStatementParser(AbcStatementParser):

    def __init__(self, parser):
        super().__init__(parser)
        self.bracket_stack = Stack()
        self.statement = Statement()
        self.body_content = []
        self.bodies_content = []

    def accept(self):

        if self.token().type == TokenType.Identifier and self.parser.index < len(
                self.parser.body) - 1 and self.token(offset=1).type == TokenType.Lp:
            # 添加方法名节点
            self.statement.add(self.token())
            # 移到左括号
            self.move()
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
                    if self.token().type == TokenType.Comma and self.bracket_stack.count() == 1:
                        self.bodies_content.append(self.body_content.copy())
                        self.body_content.clear()
                    else:
                        self.body_content.append(self.token())
            self.bodies_content.append(self.body_content)
            from edkrule.interpreter.parse.parser import Parser
            for i, body in enumerate(self.bodies_content):
                if len(body) == 0: continue
                parser = Parser(body).parse()
                self.statement.add(parser.statement)
                if i != len(self.bodies_content) - 1:
                    comma = Token(TokenType.Comma, ",")
                    self.statement.add(comma)
            self.statement.add(self.token())
            self.move()
            if not self.statement.empty():
                self.parser.statement.add(self.statement)
            return True

        return False
