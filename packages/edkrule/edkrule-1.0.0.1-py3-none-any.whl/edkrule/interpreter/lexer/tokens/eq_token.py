from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class EqToken:
    @staticmethod
    def accept(lexer, char: str):
        if lexer.state == DfaState.Assignment and Character.isassign(char):
            lexer.token_text += char
            lexer.state = DfaState.Eq
            return True
        return False