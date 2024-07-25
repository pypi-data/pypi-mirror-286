from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class FalseState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.False1:
            lexer.token_text += char
            lexer.state = DfaState.False2 if Character.isa(char) else DfaState.Identifier
            # lexer.state = DfaState.False2
            return True
        elif state == DfaState.False2:
            lexer.token_text += char
            lexer.state = DfaState.False3 if Character.isl(char) else DfaState.Identifier
            # lexer.state = DfaState.False3
            return True
        elif state == DfaState.False3:
            lexer.token_text += char
            lexer.state = DfaState.False4 if Character.iss(char) else DfaState.Identifier
            # lexer.state = DfaState.False4
            return True
        elif state == DfaState.False4:
            lexer.token_text += char
            lexer.state = DfaState.False5 if Character.ise(char) else DfaState.Identifier
            # lexer.state = DfaState.False5
            return True
        elif state == DfaState.False5:
            if Character.isseparators(char) or Character.iscolon(char):
                lexer.token_type = TokenType.FALSE
                lexer.init_token(char)
            else:
                lexer.token_text += char
                lexer.state = DfaState.Identifier
            return True

        return False
