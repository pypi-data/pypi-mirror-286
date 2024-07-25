from io import StringIO

from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.utils.format.formater import Formater


class BlankFormater(Formater):
    def initialize(self, string) -> str:
        """
        格式化，去除空格
        :param string:
        :type string:
        :return:
        :rtype:
        """
        lexer = Lexer()
        lexer.tokenize(StringIO(string))
        text = "".join([e.text for e in list(filter(lambda e: e.type != TokenType.Blank, lexer.token_list))])
        return text
