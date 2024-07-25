

from edkrule.engine.finder.finder import Finder
from edkrule.interpreter.lexer.tokens.token import Token


class FinderByRid(Finder):
    def find(self, expression, rid):
        if rid == expression.rid:
            return expression
        else:
            for body in expression.body:
                if type(body) != Token:
                    rule = body.find(FinderByRid(), rid)
                    if rule is not None: return rule
