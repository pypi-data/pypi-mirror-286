
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class RpState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Rp:
            lexer.token_type = TokenType.Rp
            lexer.init_token(char)
            return True
        return False
