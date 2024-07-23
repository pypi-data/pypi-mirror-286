from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class LeToken:
    @staticmethod
    def accept(lexer, char: str):
        if lexer.state == DfaState.Lt:
            if Character.isassign(char):
                lexer.state = DfaState.Le
                lexer.token_type = TokenType.Le
                lexer.token_text += char
                return True
        return False
