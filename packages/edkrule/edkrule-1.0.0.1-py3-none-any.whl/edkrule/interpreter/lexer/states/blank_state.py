from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class BlankState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Blank:
            # lexer.token_text += char
            lexer.token_type = TokenType.Blank
            lexer.init_token(char)
            return True
        return False
