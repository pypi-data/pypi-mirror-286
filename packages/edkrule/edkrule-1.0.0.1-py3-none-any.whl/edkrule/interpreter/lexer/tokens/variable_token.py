from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class VariableToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isdollor(char):
            lexer.state = DfaState.Var
            lexer.token_text += char
            return True
        return False
