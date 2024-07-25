from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class GtToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isgreat(char):
            lexer.state = DfaState.Gt
            lexer.token_type = TokenType.Gt
            lexer.token_text += char
            return True
        return False
