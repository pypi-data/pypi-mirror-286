from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class QuestionToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isquestion(char):
            lexer.token_text += char
            lexer.state = DfaState.Question
            return True
        return False