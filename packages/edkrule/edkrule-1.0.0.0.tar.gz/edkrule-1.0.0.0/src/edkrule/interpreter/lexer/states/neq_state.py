from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class NeqState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.NEq:
            if Character.isassign(char):
                lexer.token_text += char
                lexer.state = DfaState.Nidentity
            else:
                lexer.token_type = TokenType.NEq
                lexer.init_token(char)
            return True
        return False
