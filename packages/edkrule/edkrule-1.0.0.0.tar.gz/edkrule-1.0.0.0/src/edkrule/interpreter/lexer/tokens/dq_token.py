from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class DqToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isdoublequotation(char):
            lexer.token_text += char
            lexer.state = DfaState.Dq
            return True
        return False