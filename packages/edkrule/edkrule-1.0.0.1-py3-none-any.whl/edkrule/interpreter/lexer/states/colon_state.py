from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class ColonState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Colon:
            lexer.token_type = TokenType.Colon
            lexer.init_token(char)
            return True
        return False