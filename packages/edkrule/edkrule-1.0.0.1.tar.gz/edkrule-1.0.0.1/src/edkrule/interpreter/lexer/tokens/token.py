from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class Token:
    def __init__(self, t_type: TokenType = TokenType.Initial, t_text: str = ""):
        self._type: TokenType = t_type
        self._text: str = t_text

    @property
    def type(self): return self._type

    @type.setter
    def type(self, value): self._type = value

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value): self._text = value

    def append(self, char: str):
        self._text = self._text + char
