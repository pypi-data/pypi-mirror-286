from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState


class IdentifierState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Identifier:
            if Character.isalpha(char) or Character.isdigit(char) or Character.isdot(char):
                lexer.token_text += char
            else:
                lexer.state = lexer.init_token(char)
            return True
        return False
