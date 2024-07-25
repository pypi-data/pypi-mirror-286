from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class AwaysEqState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.AwaysEq:
            lexer.token_type = TokenType.AwaysEq
            lexer.init_token(char)
            return True

        return False