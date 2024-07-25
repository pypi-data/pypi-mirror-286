from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.false_token import FalseToken

from edkrule.interpreter.lexer.tokens.true_token import TrueToken


class IdentifierToken:
    @staticmethod
    def accept(lexer, char: str):
        if Character.isalpha(char):
            lexer.state = DfaState.Identifier
            lexer.token_type = TokenType.Identifier
            for t in [TrueToken, FalseToken]:
                if t.accept(lexer, char): return True

            lexer.token_text += char
            return True
        return False
