from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class PlusState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Plus:
            if Character.isplus(char):
                lexer.token_text += char
                lexer.state = DfaState.DPlus
            elif Character.isassign(char):
                lexer.token_text += char
                lexer.state = DfaState.PlusEq
            else:
                lexer.token_type = TokenType.Plus
                lexer.init_token(char)
            return True
        return False