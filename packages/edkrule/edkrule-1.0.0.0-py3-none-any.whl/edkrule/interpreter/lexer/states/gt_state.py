from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class GtState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Gt and Character.isassign(char):
            lexer.token_text += char
            lexer.state = DfaState.Ge
            return True
        elif state == DfaState.Gt:
            if Character.isdigit(char):
                lexer.state = DfaState.RealNumber
            else:
                lexer.state = DfaState.Identifier
            lexer.init_token(char)
            return True
        return False
