from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class LtState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Lt and Character.isassign(char):
            lexer.token_text += char
            lexer.state = DfaState.Le
            return True
        elif state == DfaState.Lt:
            if Character.isdigit(char):
                lexer.state = DfaState.RealNumber
            else:
                lexer.state = DfaState.Identifier
            lexer.init_token(char)
            return True
        return False