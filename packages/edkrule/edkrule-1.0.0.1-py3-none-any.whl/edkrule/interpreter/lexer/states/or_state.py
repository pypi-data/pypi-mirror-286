from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class OrState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Or:
            # lexer.token_text += char
            lexer.token_type = TokenType.Or
            lexer.init_token(char)
            return True
        return False
