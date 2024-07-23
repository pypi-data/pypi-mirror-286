from edkrule.interpreter.lexer.dfa_state import DfaState


class InitialState:

    @staticmethod
    def accept(lexer, char: str, state: DfaState):
        if state == DfaState.Initial:
            return lexer.init_token(char)
