from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class BiteOrState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.ByteOr and Character.isL(char):
            lexer.token_text += char
            lexer.state = DfaState.Or
            return True
        elif state == DfaState.ByteOr:
            if Character.isseparators(char) or Character.iskeyword(char):
                lexer.token_type = TokenType.ByteOr
                lexer.init_token(char)
            else:
                lexer.token_text += char
                lexer.state = DfaState.Identifier
            return True
        return False