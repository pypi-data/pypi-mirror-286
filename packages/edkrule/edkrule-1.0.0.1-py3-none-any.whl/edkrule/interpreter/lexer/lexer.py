from io import StringIO

from edkrule.interpreter.lexer.character import Character
from edkrule.interpreter.lexer.dfa_state import DfaState
from edkrule.interpreter.lexer.states.and_state import AndState
from edkrule.interpreter.lexer.states.assign_state import AssignState
from edkrule.interpreter.lexer.states.aways_eq_state import AwaysEqState
from edkrule.interpreter.lexer.states.bite_and_state import BiteAndState
from edkrule.interpreter.lexer.states.bite_or_state import BiteOrState
from edkrule.interpreter.lexer.states.blank_state import BlankState
from edkrule.interpreter.lexer.states.colon_state import ColonState
from edkrule.interpreter.lexer.states.comma_state import CommaState
from edkrule.interpreter.lexer.states.d_minus_state import DMinusState
from edkrule.interpreter.lexer.states.d_plus_state import DPlusState
from edkrule.interpreter.lexer.states.divide_state import DivideState
from edkrule.interpreter.lexer.states.dot_state import DotState
from edkrule.interpreter.lexer.states.dq_state import DQState
from edkrule.interpreter.lexer.states.ep_state import EpState
from edkrule.interpreter.lexer.states.eq_minus_state import EqMinusState
from edkrule.interpreter.lexer.states.eq_plus_state import EqPlusState
from edkrule.interpreter.lexer.states.eq_state import EqState
from edkrule.interpreter.lexer.states.false_state import FalseState
from edkrule.interpreter.lexer.states.ge_state import GeState
from edkrule.interpreter.lexer.states.gt_state import GtState
from edkrule.interpreter.lexer.states.identifier_state import IdentifierState
from edkrule.interpreter.lexer.states.initial_state import InitialState
from edkrule.interpreter.lexer.states.le_state import LeState
from edkrule.interpreter.lexer.states.lp_state import LpState
from edkrule.interpreter.lexer.states.lt_state import LtState
from edkrule.interpreter.lexer.states.minus_eq_state import MinusEqState
from edkrule.interpreter.lexer.states.minus_state import MinusState
from edkrule.interpreter.lexer.states.multiply_state import MultiplyState
from edkrule.interpreter.lexer.states.neq_state import NeqState
from edkrule.interpreter.lexer.states.nidentity_state import NidentityState
from edkrule.interpreter.lexer.states.or_state import OrState
from edkrule.interpreter.lexer.states.plus_eq_state import PlusEqState
from edkrule.interpreter.lexer.states.plus_state import PlusState
from edkrule.interpreter.lexer.states.question_state import QuestionState
from edkrule.interpreter.lexer.states.real_number_state import RealNumberState
from edkrule.interpreter.lexer.states.rp_state import RpState
from edkrule.interpreter.lexer.states.sq_state import SQState
from edkrule.interpreter.lexer.states.true_state import TrueState
from edkrule.interpreter.lexer.states.variable_state import VariableState
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.lexer.tokens.assign_token import AssignToken
from edkrule.interpreter.lexer.tokens.bite_and_token import BiteAndToken
from edkrule.interpreter.lexer.tokens.bite_or_token import BiteOrToken
from edkrule.interpreter.lexer.tokens.blank_token import BlankToken
from edkrule.interpreter.lexer.tokens.colon_token import ColonToken
from edkrule.interpreter.lexer.tokens.comma_token import CommaToken
from edkrule.interpreter.lexer.tokens.divide_token import DivideToken
from edkrule.interpreter.lexer.tokens.dot_token import DotToken
from edkrule.interpreter.lexer.tokens.dq_token import DqToken
from edkrule.interpreter.lexer.tokens.ep_token import EpToken
from edkrule.interpreter.lexer.tokens.false_token import FalseToken
from edkrule.interpreter.lexer.tokens.gt_token import GtToken
from edkrule.interpreter.lexer.tokens.identifier_token import IdentifierToken
from edkrule.interpreter.lexer.tokens.lp_token import LpToken
from edkrule.interpreter.lexer.tokens.lt_token import LtToken
from edkrule.interpreter.lexer.tokens.minus_token import MinusToken
from edkrule.interpreter.lexer.tokens.multiply_token import MultiplyToken
from edkrule.interpreter.lexer.tokens.neq_token import NeqToken
from edkrule.interpreter.lexer.tokens.plus_token import PlusToken
from edkrule.interpreter.lexer.tokens.question_token import QuestionToken
from edkrule.interpreter.lexer.tokens.realnumber_token import RealNumberToken
from edkrule.interpreter.lexer.tokens.rp_token import RpToken
from edkrule.interpreter.lexer.tokens.sq_token import SqToken
from edkrule.interpreter.lexer.tokens.token import Token
from edkrule.interpreter.lexer.tokens.true_token import TrueToken
from edkrule.interpreter.lexer.tokens.variable_token import VariableToken


class Lexer:
    def __init__(self):
        self.token_list = []
        self.token_type = None
        self.token_text = ""
        self.state = DfaState.Initial

        # 为了Variable 的 *.* 方式
        self.dot_numer = 0
        self.next_dot = False

    def reset(self):
        self.token_type = None
        self.token_text = ""

    def clean(self):
        self.reset()
        self.state = DfaState.Initial
        self.token_list = []

    def init_token(self, char: str) -> DfaState:
        if self.token_text:
            token = Token(self.token_type, self.token_text)
            self.token_list.append(token)
            self.reset()

        self.state = DfaState.Initial
        for t in [IdentifierToken, BlankToken, BiteAndToken, BiteOrToken, RealNumberToken,
                  PlusToken, MinusToken, ColonToken, SqToken, DqToken, CommaToken, QuestionToken,
                  LpToken, RpToken, VariableToken, GtToken, LtToken, EpToken, NeqToken, AssignToken,
                  MultiplyToken, DivideToken, DotToken]:
            if t.accept(self, char):
                break
        return self.state

    def tokenize(self, code):
        self.clean()
        while True:
            char = code.read(1)
            if not char:
                self.last(char)
                break
            for s in [InitialState, IdentifierState, TrueState, FalseState, BlankState,
                      BiteAndState, AndState, BiteOrState, OrState, RealNumberState, PlusState,
                      DPlusState, PlusEqState, MinusState, DMinusState, MinusEqState, ColonState,
                      SQState, DQState, CommaState, QuestionState, LpState, RpState, VariableState,
                      GtState, GeState, LtState, LeState, EpState, NeqState, NidentityState, AssignState,
                      EqState, EqPlusState, EqMinusState, AwaysEqState, DivideState, MultiplyState, DotState]:
                if s.accept(self, char, self.state):
                    break

    def last(self, char):
        if self.state == DfaState.True4:
            self.token_type = TokenType.TRUE
        elif self.state == DfaState.Identifier:
            self.token_type = TokenType.Identifier
        elif self.state == DfaState.False5:
            self.token_type = TokenType.FALSE
        elif self.state == DfaState.Blank:
            self.token_type = TokenType.Blank
        elif self.state == DfaState.ByteAnd:
            self.token_type = TokenType.ByteAnd
        elif self.state == DfaState.And:
            self.token_type = TokenType.And
        elif self.state == DfaState.ByteOr:
            self.token_type = TokenType.ByteOr
        elif self.state == DfaState.Or:
            self.token_type = TokenType.Or
        elif self.state == DfaState.RealNumber:
            self.token_type = TokenType.RealNumber
        elif self.state == DfaState.Plus:
            self.token_type = TokenType.Plus
        elif self.state == DfaState.DPlus:
            self.token_type = TokenType.DPlus
        elif self.state == DfaState.PlusEq:
            self.token_type = TokenType.PlusEq
        elif self.state == DfaState.Minus:
            self.token_type = TokenType.Minus
        elif self.state == DfaState.DMinus:
            self.token_type = TokenType.DMinus
        elif self.state == DfaState.MinusEq:
            self.token_type = TokenType.MinusEq
        elif self.state == DfaState.Colon:
            self.token_type = TokenType.Colon
        elif self.state == DfaState.Comma:
            self.token_type = TokenType.Comma
        elif self.state == DfaState.Question:
            self.token_type = TokenType.Question
        elif self.state == DfaState.Lp:
            self.token_type = TokenType.Lp
        elif self.state == DfaState.Rp:
            self.token_type = TokenType.Rp
        elif self.state == DfaState.Var:
            self.token_type = TokenType.Variable
            self.dot_numer = 0
            self.next_dot = False
        if self.state != DfaState.Initial:
            self.init_token(char)

    def display(self):
        print([(t.type, t.text) for t in self.token_list])


if __name__ == '__main__':
    lexer = Lexer()
    # string = StringIO("()")
    #
    # string = StringIO("(1+2)")
    #
    # string = StringIO("(\"ass\" + \"1+2\")")
    #
    # string = StringIO("('ass' + '1+2')")
    string = StringIO("a!=''")

    # string = StringIO("1!==2")

    lexer.tokenize(string)
    for t in lexer.token_list:
        print(t.type, t.text)
