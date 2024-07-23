from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class EpState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if Character.isexclamationpoint(char):
            lexer.token_text += char
            lexer.token_type = TokenType.Ep
            lexer.state = DfaState.Ep
            return True
            # lexer.init_token(char)
        elif lexer.state == DfaState.Ep and Character.isassign(char):
            lexer.token_text += char
            # lexer.token_type = TokenType.NEq
            lexer.state = DfaState.NEq
            return True
        return False

