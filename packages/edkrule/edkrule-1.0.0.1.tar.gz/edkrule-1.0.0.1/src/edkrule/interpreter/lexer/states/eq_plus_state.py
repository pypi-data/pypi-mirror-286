from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class EqPlusState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.EqPlus:
            lexer.token_type = TokenType.EqPlus
            lexer.init_token(char)
            return True
        return False