from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class RpToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isrightparentheses(char):
            lexer.token_text += char
            lexer.state = DfaState.Rp
            return True
        return False