from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class EqState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Eq and Character.isassign(char):
            lexer.token_text += char
            lexer.state = DfaState.AwaysEq
            return True
        elif state == DfaState.Eq:
            lexer.token_type = TokenType.Eq
            lexer.init_token(char)
            return True
        return False
