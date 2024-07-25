from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class EqMinusState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.EqMinus:
            lexer.token_type = TokenType.EqMinus
            lexer.init_token(char)
            return True
        return False
