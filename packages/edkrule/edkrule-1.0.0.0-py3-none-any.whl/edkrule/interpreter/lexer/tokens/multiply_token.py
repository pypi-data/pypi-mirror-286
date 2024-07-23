from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class MultiplyToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.ismultiply(char):
            lexer.token_text += char
            lexer.state = DfaState.Multipy
            return True
        return False
