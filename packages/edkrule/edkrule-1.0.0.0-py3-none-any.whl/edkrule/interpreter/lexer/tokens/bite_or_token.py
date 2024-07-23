from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class BiteOrToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isL(char):
            lexer.token_text += char
            lexer.state = DfaState.ByteOr
            return True
        return False
