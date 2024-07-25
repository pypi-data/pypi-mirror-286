from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.token_type import TokenType


class VariableState:
    # dot_numer = 0
    # next_dot = False

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Var:
            if lexer.dot_numer > 1:
                if Character.isrightparentheses(char) or Character.iscomma(char) or (
                        Character.isoperate(char) and lexer.next_dot is False):
                    lexer.token_type = TokenType.Variable
                    lexer.dot_numer = 0
                    lexer.init_token(char)
                else: lexer.token_text += char

                lexer.next_dot = False
            else:
                if Character.isdot(char):
                    lexer.dot_numer += 1
                    lexer.next_dot = True
                else: lexer.next_dot = False
                lexer.token_text += char
            return True
        return False
