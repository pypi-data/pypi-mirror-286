from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class BlankToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isblank(char):
            lexer.token_text += char
            lexer.state = DfaState.Blank
            return True
        return False
