from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class RealNumberState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.RealNumber:
            if Character.isdigit(char) or Character.isdot(char):
                lexer.token_text += char
            # elif Character.isseparators(char) or Character.isplus(char) or Character.isminus(char):
            else:
                if Character.isdot(lexer.token_text[-1]):
                    raise Exception(f'{lexer.token_text} is invalid number')
                lexer.token_type = TokenType.RealNumber
                lexer.init_token(char)
            return True
        return False
