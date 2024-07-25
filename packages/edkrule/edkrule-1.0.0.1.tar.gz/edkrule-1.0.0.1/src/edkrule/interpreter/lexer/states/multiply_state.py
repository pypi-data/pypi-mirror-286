from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class MultiplyState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Multipy:
            lexer.token_type = TokenType.Multipy
            lexer.init_token(char)
            return True
        return False
