from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class SqToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.issinglequotation(char):
            lexer.token_text += char
            lexer.state = DfaState.Sq
            return True
        return False