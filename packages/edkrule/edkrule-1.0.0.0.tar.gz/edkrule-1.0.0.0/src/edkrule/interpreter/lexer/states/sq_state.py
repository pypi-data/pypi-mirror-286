from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class SQState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Sq:
            if Character.issinglequotation(char):
                lexer.token_text += char
                lexer.token_type = TokenType.Identifier
                lexer.state = DfaState.Identifier
                # lexer.init_token(char)
            else:
                lexer.token_text += char
            return True
        return False
