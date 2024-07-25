from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class GeToken:
    @staticmethod
    def accept(lexer, char: str):
        if lexer.state == DfaState.Gt:
            if Character.isassign(char):
                lexer.state = DfaState.Ge
                lexer.token_type = TokenType.Ge
                lexer.token_text += char
                return True
        return False
