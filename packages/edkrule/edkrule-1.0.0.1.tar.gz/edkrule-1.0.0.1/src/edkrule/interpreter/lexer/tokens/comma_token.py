from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class CommaToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.iscomma(char):
            lexer.token_text += char
            lexer.state = DfaState.Comma
            return True
        return False