from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class DotToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isdot(char):
            lexer.token_text += char
            lexer.state = DfaState.Dot
            return True
        return False
