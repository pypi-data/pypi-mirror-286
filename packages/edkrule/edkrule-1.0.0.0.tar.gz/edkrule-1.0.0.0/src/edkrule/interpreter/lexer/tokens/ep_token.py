from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class EpToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isexclamationpoint(char):
            lexer.token_text += char
            lexer.state = DfaState.Ep
            return True
        return False