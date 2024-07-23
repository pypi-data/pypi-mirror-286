
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class LpState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Lp:
            lexer.token_type = TokenType.Lp
            lexer.init_token(char)
            return True
        return False
