from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class DotState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Dot:
            lexer.token_type = TokenType.Dot
            lexer.init_token(char)
            return True
        return False
