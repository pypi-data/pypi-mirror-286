from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class AssignToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isassign(char):
            lexer.token_text += char
            lexer.token_type = TokenType.Assignment
            lexer.state = DfaState.Assignment
            return True
        return False
