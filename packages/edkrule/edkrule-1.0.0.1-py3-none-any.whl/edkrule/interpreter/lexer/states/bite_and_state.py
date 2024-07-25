from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class BiteAndState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.ByteAnd and Character.isand(char):
            lexer.token_text += char
            lexer.state = DfaState.And
            return True
        elif state == DfaState.ByteAnd:
            if Character.isseparators(char) or Character.iskeyword(char):
                lexer.token_type = TokenType.ByteAnd
                lexer.init_token(char)
            else:
                lexer.token_text += char
                lexer.state = DfaState.Identifier
            return True
        return False
