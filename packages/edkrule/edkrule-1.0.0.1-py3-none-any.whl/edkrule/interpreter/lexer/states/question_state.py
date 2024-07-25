
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class QuestionState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Question:
            lexer.token_type = TokenType.Question
            lexer.init_token(char)
            return True
        return False
