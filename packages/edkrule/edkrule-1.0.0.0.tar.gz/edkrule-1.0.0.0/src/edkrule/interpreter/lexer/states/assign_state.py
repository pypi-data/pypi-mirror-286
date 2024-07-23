from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class AssignState:
    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Assignment and Character.isassign(char):
            lexer.token_text += char
            lexer.state = DfaState.Eq
            return True
        elif state == DfaState.Assignment and Character.isplus(char):
            lexer.token_text += char
            lexer.state = DfaState.EqPlus
            return True
        elif state == DfaState.Assignment and Character.isminus(char):
            lexer.token_text += char
            lexer.state = DfaState.EqMinus
            return True
        elif state == DfaState.Assignment:
            if Character.isseparators(char) or Character.iskeyword(char) or Character.isdigit(
                    char) or Character.isalpha(char):
                lexer.token_type = TokenType.Assignment
                lexer.init_token(char)
            else:
                lexer.token_text += char
                lexer.state = DfaState.Identifier
            return True


        return False
        # if state == DfaState.Assignment:
        #     # lexer.token_text += char
        #     lexer.token_type = TokenType.Assignment
        #     lexer.init_token(char)
        #     return True
        # return False
