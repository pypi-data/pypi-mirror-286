
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class CommaState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Comma:
            lexer.token_type = TokenType.Comma
            lexer.init_token(char)
            return True
        return False
