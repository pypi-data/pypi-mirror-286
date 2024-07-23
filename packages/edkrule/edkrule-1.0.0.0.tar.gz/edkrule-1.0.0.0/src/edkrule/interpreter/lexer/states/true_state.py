from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class TrueState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.True1:
            lexer.token_text += char
            lexer.state = DfaState.True2 if Character.isr(char) else DfaState.Identifier
            # lexer.state = DfaState.True2
            return True
        elif state == DfaState.True2:
            lexer.token_text += char
            lexer.state = DfaState.True3 if Character.isu(char) else DfaState.Identifier
            # lexer.state = DfaState.True3
            return True
        elif state == DfaState.True3:
            lexer.token_text += char
            lexer.state = DfaState.True4 if Character.ise(char) else DfaState.Identifier
            # lexer.state = DfaState.True4
            return True
        elif state == DfaState.True4:
            if Character.isseparators(char) or Character.iscolon(char):
                lexer.token_type = TokenType.TRUE
                lexer.init_token(char)
            else:
                lexer.token_text += char
                lexer.state = DfaState.Identifier
            return True
        return False


