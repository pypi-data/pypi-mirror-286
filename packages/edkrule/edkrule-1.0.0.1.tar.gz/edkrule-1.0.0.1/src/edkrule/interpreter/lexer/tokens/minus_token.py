from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class MinusToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isminus(char):
            lexer.token_text += char
            lexer.state = DfaState.Minus
            return True
        return False
