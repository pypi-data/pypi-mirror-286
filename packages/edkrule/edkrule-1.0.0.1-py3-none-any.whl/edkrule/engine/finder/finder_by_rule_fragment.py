from io import StringIO

from edkrule.engine.finder.finder import Finder
from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.token import Token


class FinderByRuleFragment(Finder):
    def __init__(self, formate=None):
        self._format = formate

    def find(self, expression, rule_fragment_text):
        if self._format:
            rule_fragment_text = self._format.initialize(rule_fragment_text)
        if rule_fragment_text == expression.text:
            return expression
        else:
            for body in expression.body:
                if type(body) != Token:
                    rule = body.find(FinderByRuleFragment(self._format), rule_fragment_text)
                    if rule is not None: return rule

    # def format(self, rule_fragment_text):
    #     lexer = Lexer()
    #     lexer.tokenize(StringIO(rule_fragment_text))
    #     text = "".join([e.text for e in list(filter(lambda e: e.type != TokenType.Blank, l.token_list))])
    #     return text
