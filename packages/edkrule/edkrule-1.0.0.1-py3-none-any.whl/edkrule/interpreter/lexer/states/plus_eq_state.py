
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class PlusEqState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.PlusEq:
            lexer.token_type = TokenType.PlusEq
            lexer.init_token(char)
            return True
        return False
