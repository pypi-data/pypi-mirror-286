import dataclasses

from edkrule.interpreter.expression.bracket_enum import BracketEnum
from edkrule.interpreter.lexer.tokens.token import Token


@dataclasses.dataclass
class Bracket:
    type: BracketEnum
    token: Token
