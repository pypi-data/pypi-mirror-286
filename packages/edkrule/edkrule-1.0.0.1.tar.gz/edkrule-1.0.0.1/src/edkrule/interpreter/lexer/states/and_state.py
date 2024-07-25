from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class AndState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.And:
            # lexer.token_text += char
            lexer.token_type = TokenType.And
            lexer.init_token(char)
            return True
        return False
