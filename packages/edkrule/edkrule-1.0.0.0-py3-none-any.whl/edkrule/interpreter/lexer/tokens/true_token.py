from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class TrueToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isalpha(char) and Character.ist(char):
            lexer.state = DfaState.True1
            lexer.token_text += char
            return True
        # elif Character.isalpha(char) and Character.isr(char) and lexer.state == DfaState.True1:
        #     lexer.state = DfaState.True2
        #     lexer.token_text += char
        #     return True
        # elif Character.isalpha(char) and Character.isu(char) and lexer.state == DfaState.True2:
        #     lexer.state = DfaState.True3
        #     lexer.token_text += char
        #     return True
        # elif Character.isalpha(char) and Character.ise(char) and lexer.state == DfaState.True3:
        #     lexer.state = DfaState.True4
        #     lexer.token_text += char
        #     lexer.token_type = TokenType.TRUE
        #     return True
        return False
