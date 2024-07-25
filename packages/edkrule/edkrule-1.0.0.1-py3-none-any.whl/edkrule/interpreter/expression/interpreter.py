from edkrule.interpreter.expression.bracket import Bracket
from edkrule.interpreter.expression.bracket_enum import BracketEnum
from edkrule.interpreter.expression.categorize import Categorize
from edkrule.interpreter.expression.expression import Expression
from edkrule.interpreter.expression.priority import Priority
from edkrule.interpreter.expression.stack import Stack
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.token import Token
from edkrule.interpreter.parse.statement import Statement


class Interpreter:
    def __init__(self):
        self._expression_stack = Stack()
        self._op_stack = Stack()
        self._bracket_stack = Stack()
        self.cache = list()

    def is_op(self, stmt):
        return Categorize.is_op(stmt)

    def is_exp(self, stmt):
        return Categorize.is_exp(stmt)

    def is_stmt(self, stmt):
        return Categorize.is_stmt(stmt)

    def interpret(self, statement: Statement):
        i = 0
        while i < len(statement.body):
            stmt = statement.body[i]
            if self.is_stmt(stmt):
                self._expression_stack.push(Interpreter().interpret(stmt))
            if self.is_exp(stmt):
                self._expression_stack.push(stmt)
            if stmt.type in [TokenType.Lp]:
                pre_stmt = statement.body[i - 1]
                be = BracketEnum.Function if pre_stmt.type == TokenType.Identifier else BracketEnum.Calculate
                self._bracket_stack.push(Bracket(be, stmt))
            if stmt.type in [TokenType.Rp]:
                if self._bracket_stack.count() == 0 or self._bracket_stack.top().token.type != TokenType.Lp:
                    raise Exception(f"{''.join([t.text for t in statement.body[0:i]])} () is not pair")
                sub_expressions = self._expression_stack.pop_until(condition=lambda e: e.type == TokenType.Lp)
                expression = Expression([])
                for sub in sub_expressions:
                    sub_expression = Interpreter().interpret(sub) if sub.type == TokenType.Statement else sub
                    expression.append(sub_expression)
                if self._bracket_stack.top().type == BracketEnum.Function:
                    if self._expression_stack.top() is not None:
                        if self._expression_stack.top().type == TokenType.Identifier:
                            expression.name = self._expression_stack.pop()
                self._expression_stack.push(expression)
                self._bracket_stack.pop()
            if self.is_op(stmt):
                if self._bracket_stack.count() != 0:
                    self._expression_stack.push(stmt)
                else:
                    if self._op_stack.count() == 0 or Priority.gt(stmt, self._op_stack.top()):
                        self._op_stack.push(stmt)
                        if stmt.type == TokenType.Question:
                            i = self.ternary_operator(i, statement.body)

                    else:
                        expression = self.binary_operator()
                        self._expression_stack.push(expression)
                        self._op_stack.push(stmt)
                        if stmt.type == TokenType.Question:
                            i = self.ternary_operator(i, statement.body)
            i += 1
        while self._op_stack.count() != 0:
            expression = self.binary_operator()
            self._expression_stack.push(expression)
        return self._expression_stack.pop()

    def binary_operator(self):
        op_refs = self._expression_stack.pops(2)
        body = [op_refs[0], self._op_stack.pop(), op_refs[1]]
        return Expression(body)

    def ternary_operator(self, i: int, content: list):
        expression_left = Interpreter().interpret(statement=content[i + 1])
        comma = content[i + 2]
        expression_right = Interpreter().interpret(statement=content[i + 3])
        expression = Expression([])
        expression.append(self._expression_stack.pop())
        expression.append(self._op_stack.pop())
        expression.append(expression_left)
        expression.append(comma)
        expression.append(expression_right)
        expression.name = Token(t_type=TokenType.Identifier, t_text="TernaryOperator")
        self._expression_stack.push(expression)
        return i + 3
