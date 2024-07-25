from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class ColonToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.iscolon(char):
            lexer.token_text += char
            lexer.state = DfaState.Colon
            return True
        return False
