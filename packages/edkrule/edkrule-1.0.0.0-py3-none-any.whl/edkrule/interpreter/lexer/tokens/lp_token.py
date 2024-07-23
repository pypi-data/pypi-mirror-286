from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class LpToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isleftparentheses(char):
            lexer.token_text += char
            lexer.state = DfaState.Lp
            return True
        return False