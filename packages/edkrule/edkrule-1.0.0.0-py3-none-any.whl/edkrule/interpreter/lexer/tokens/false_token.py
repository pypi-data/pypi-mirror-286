from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.token import Token


class FalseToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isalpha(char) and Character.isf(char):
            lexer.token_text += char
            lexer.state = DfaState.False1
            return True
        # elif Character.isalpha(char) and Character.isa(char) and lexer.state == DfaState.False1:
        #     lexer.token_text += char
        #     lexer.state = DfaState.False2
        #     return True
        # elif Character.isalpha(char) and Character.isl(char) and lexer.state == DfaState.False2:
        #     lexer.token_text += char
        #     lexer.state = DfaState.False3
        #     return True
        # elif Character.isalpha(char) and Character.iss(char) and lexer.state == DfaState.False3:
        #     lexer.token_text += char
        #     lexer.state = DfaState.False4
        #     return True
        # elif Character.isalpha(char) and Character.ise(char) and lexer.state == DfaState.False4:
        #     lexer.token_text += char
        #     lexer.state = DfaState.False5
        #     lexer.token_type = TokenType.FALSE
        #     return True
        return False
