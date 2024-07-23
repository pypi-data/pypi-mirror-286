from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class DivideToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isdivide(char):
            lexer.token_text += char
            lexer.state = DfaState.Divide
            return True
        return False
