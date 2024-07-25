from io import StringIO

from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.tokens.token import Token
from edkrule.interpreter.parse.statement_parser.ternary_statement_parser import TernaryStatementParser

from edkrule.interpreter.parse.statement import Statement
from edkrule.interpreter.parse.statement_parser.bracket_statement_parser import BracketStatementParser
from edkrule.interpreter.parse.statement_parser.colon_statement_parser import ColonStatementParser
from edkrule.interpreter.parse.statement_parser.end_statement_parser import EndStatementParser
from edkrule.interpreter.parse.statement_parser.function_statement_parser import FunctionStatementParser
from edkrule.interpreter.parse.statement_parser.normal_statement_parser import NormalStatementParser
from edkrule.interpreter.parse.statement_parser.question_statement_parser import QuestionStatementParser
from edkrule.utils.stack import Stack


class Parser:
    def __init__(self, parse_tokens: list[Token]):
        self.statement = Statement()
        self.body = parse_tokens
        self.index = 0
        self.ternary_stack = Stack()

    def parse2(self):
        while self.index <= len(self.body) - 1:
            for exp in [FunctionStatementParser(self),
                        BracketStatementParser(self),
                        QuestionStatementParser(self),
                        ColonStatementParser(self),
                        NormalStatementParser(self),
                        EndStatementParser(self)
                        ]:
                if exp.accept(): continue
        return self

    def parse(self):
        while self.index <= len(self.body) - 1:
            for exp in [FunctionStatementParser(self),
                        BracketStatementParser(self),
                        TernaryStatementParser(self),
                        NormalStatementParser(self),
                        EndStatementParser(self)
                        ]:
                if exp.accept(): continue
        return self


def case1():
    s = StringIO("a(1+2+b(2))")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse2()
    print(es.statement)


def case0():
    s = StringIO("b(2,3+1,4)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case2():
    s = StringIO("b(2,3+1,4)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case3():
    s = StringIO("date((1+2)+3==(4+5), year(\"xxxx\"), 9+10)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case4():
    s = StringIO("a+b==1?2+3:4+1+2")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case5():
    s = StringIO("taDate(a+b==1?2+3:4+1+2,111)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case6():
    s = StringIO("taDate(a+b==1?(2+3):4+1+2,111)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case7():
    s = StringIO("taDate(a+b==1?(data(2+3)?(x+1):ddd):4+1+2,111)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case8():
    s = StringIO("a+b==1?(data(2+3)?(x+10):ddd):4+1+2+111")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case9():
    s = StringIO(
        "autoValue((toNum($*.*.EGORRES.881)!=''&&toNum($*.*.EGORRES.879)!=''?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), \"1\"):\"\"), true)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case10():
    s = StringIO("$*.*.*=='Y'&&mustAnswer($*.Demographics.AGE)?toNum($*.Demographics.AGE)>=18:true")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)


def case11():
    s = StringIO("1==1?2==2?3:1:1")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es.statement)

def case12():
    s = StringIO("1==2?2+1:3==4?4:5")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()

def case13():
    s = StringIO("a==1?true:(x==1?y:z)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es)

def case14():
    s = StringIO("a(c())?1:b(d())")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()

def case15():
    s = StringIO("a(c())?1:b(d(1,2),x())")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es)

def case16():
    # s = StringIO("autoincrease(1,1)==3?autoincrease(1,1):autoincrease(autoincrease(1,1),1),3+1,4+1)")
    s = StringIO("a?autoincrease(1,1):autoincrease(autoincrease(1,1),1),3)")
    # s = StringIO("a(c())?1:b(d(1,2),x())")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    print(es)


if __name__ == "__main__":
   case16()