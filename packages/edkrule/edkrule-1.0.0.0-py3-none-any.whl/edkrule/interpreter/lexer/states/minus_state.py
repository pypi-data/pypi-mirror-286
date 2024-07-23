from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class MinusState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Minus:
            if Character.isminus(char):
                lexer.token_text += char
                lexer.state = DfaState.DMinus
            elif Character.isassign(char):
                lexer.token_text += char
                lexer.state = DfaState.MinusEq
            else:
                lexer.token_type = TokenType.Minus
                lexer.init_token(char)
            return True
        return False