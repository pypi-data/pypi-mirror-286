from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class DivideState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Divide:
            lexer.token_type = TokenType.Divide
            lexer.init_token(char)
            return True
        return False
