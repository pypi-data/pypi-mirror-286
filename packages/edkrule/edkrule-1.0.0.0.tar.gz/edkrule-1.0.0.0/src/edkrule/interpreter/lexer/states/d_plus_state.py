from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class DPlusState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.DPlus:
            # lexer.token_text += char
            lexer.token_type = TokenType.DPlus
            lexer.init_token(char)
            return True
        return False