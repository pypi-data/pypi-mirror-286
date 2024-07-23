
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class MinusEqState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.MinusEq:
            lexer.token_type = TokenType.MinusEq
            lexer.init_token(char)
            return True
        return False
