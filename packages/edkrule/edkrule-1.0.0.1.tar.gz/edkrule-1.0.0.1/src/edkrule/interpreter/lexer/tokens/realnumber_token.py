from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class RealNumberToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isdigit(char):
            lexer.token_text += char
            lexer.state = DfaState.RealNumber
            return True
        return False

