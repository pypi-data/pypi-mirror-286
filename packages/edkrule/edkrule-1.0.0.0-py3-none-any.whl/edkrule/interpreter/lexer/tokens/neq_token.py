from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class NeqToken:
    @staticmethod
    def accept(lexer, char: str):
        if lexer.state == DfaState.NEq:
            lexer.state = DfaState.NEq
            lexer.token_type = TokenType.NEq
            lexer.token_text += char
            return True
        return False
