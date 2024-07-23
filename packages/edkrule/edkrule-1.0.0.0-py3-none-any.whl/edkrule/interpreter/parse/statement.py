from edkrule.engine.constant import Constant
from edkrule.engine.engine import Engine
from edkrule.interpreter.expression.categorize import Categorize
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.token import Token


class Statement:
    def __init__(self):
        self.content = []
        self._engine = None

    def add(self, e):
        self.content.append(e)

    @property
    def engine(self) -> Engine:
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    def run(self):
        result = None
        if self.type == TokenType.Statement:
            raise "Statement can not run"
        if self.type == TokenType.RealNumber:
            result = self.engine.get_class(Constant.DataTypes, TokenType.RealNumber.name)().run(self.text)
        elif self.type == TokenType.Identifier:
            result = self.engine.get_class(Constant.Identifiers, self.text)().run(self.text)
        elif self.type == TokenType.TRUE or self.type == TokenType.FALSE:
            result = self.engine.get_class(Constant.DataTypes, self.text)().run(self.text)
        return result

    @property
    def type(self):
        if len(self.content) == 1: return self.content[0].type
        return TokenType.Statement

    def token(self):
        if len(self.content) == 1: return self.content[0]
        raise Exception("Only Statement contain one element support")

    @property
    def text(self):
        if len(self.content) == 1: return self.content[0].text
        return "".join([e.text for e in self.content])

    def empty(self):
        return len(self.content) == 0

    def count(self):
        return len(self.content)

    def remove(self, from_i: int):
        self.content = self.content[0:from_i + 1]

    def matrix(self, *args):
        deep = len(args)
        index = 0
        result = self.content[args[index]]
        while deep > 1:
            deep -= 1
            index += 1
            result = result.content[args[index]]

        return result

    def display(self, index: list):
        """
        测试用
        :param index:
        :type index:
        :return:
        :rtype:
        """
        if not index: print(self.text)
        for i, e in enumerate(self.content):
            pos = []
            pos.extend(index)
            pos.append(str(i))
            print("assert", f'es.statement.matrix({",".join(pos)}).text == \'{e.text}\'')
            print("assert", f'es.statement.matrix({",".join(pos)}).type == {e.type}')
            # if Categorize.is_variable(e) or Categorize.is_op(e):
            #     # exp.matrix(0).name == 'Anonymous'
            #
            # else:
            #     print("assert", f'exp.matrix({",".join(pos)}).name == \'{e.name}\'')
            #     print("assert", f'exp.matrix({",".join(pos)}).type == {e.type}')
            #     # print(",".join(pos), e.name, e.type)
            if e.type == TokenType.Statement:
                e.display(pos)
