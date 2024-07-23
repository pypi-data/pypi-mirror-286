from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class PlusToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isplus(char):
            lexer.token_text += char
            lexer.state = DfaState.Plus
            return True
        return False
