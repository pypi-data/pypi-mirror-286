from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class BiteAndToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isand(char):
            lexer.token_text += char
            lexer.state = DfaState.ByteAnd
            return True
        return False
