from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class LtToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isless(char):
            lexer.state = DfaState.Lt
            lexer.token_type = TokenType.Lt
            lexer.token_text += char
            return True
        return False
