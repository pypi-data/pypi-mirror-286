from io import StringIO

from edkrule.interpreter.expression.interpreter import Interpreter
from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.parser import Parser


def evals(stringio):
    l = Lexer()
    l.tokenize(stringio)
    es = Parser(l.token_list)
    es.parse()
    exp = Interpreter().interpret(es.statement)
    return exp


def case0():
    rule = StringIO("toDate(a,c)")
    exp = evals(rule)
    assert exp.name == 'toDate'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == 'c'
    assert exp.matrix(1).type == TokenType.Identifier
    # exp.display2([])


def case1():
    rule = StringIO("toDate(a,b,min(c,d))")
    exp = evals(rule)
    assert exp.name == 'toDate'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == 'b'
    assert exp.matrix(1).type == TokenType.Identifier
    assert exp.matrix(2).name == 'min'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == 'c'
    assert exp.matrix(2, 0).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == 'd'
    assert exp.matrix(2, 1).type == TokenType.Identifier
    # exp.display2([])


def case2():
    rule = StringIO("1+2+3")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == '1'
    assert exp.matrix(0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 1).text == '+'
    assert exp.matrix(0, 1).type == TokenType.Plus
    assert exp.matrix(0, 2).text == '2'
    assert exp.matrix(0, 2).type == TokenType.RealNumber
    assert exp.matrix(1).text == '+'
    assert exp.matrix(1).type == TokenType.Plus
    assert exp.matrix(2).text == '3'
    assert exp.matrix(2).type == TokenType.RealNumber
    # exp.display2([])


def case3():
    rule = StringIO("a==1+2")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == '=='
    assert exp.matrix(1).type == TokenType.Eq
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == '1'
    assert exp.matrix(2, 0).type == TokenType.RealNumber
    assert exp.matrix(2, 1).text == '+'
    assert exp.matrix(2, 1).type == TokenType.Plus
    assert exp.matrix(2, 2).text == '2'
    assert exp.matrix(2, 2).type == TokenType.RealNumber
    # exp.display2([])


def case4():
    rule = StringIO("a==1+(2+3)")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == '=='
    assert exp.matrix(1).type == TokenType.Eq
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == '1'
    assert exp.matrix(2, 0).type == TokenType.RealNumber
    assert exp.matrix(2, 1).text == '+'
    assert exp.matrix(2, 1).type == TokenType.Plus
    assert exp.matrix(2, 2).name == 'Anonymous'
    assert exp.matrix(2, 2).type == TokenType.Expression
    assert exp.matrix(2, 2, 0).name == 'Anonymous'
    assert exp.matrix(2, 2, 0).type == TokenType.Expression
    assert exp.matrix(2, 2, 0, 0).text == '2'
    assert exp.matrix(2, 2, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(2, 2, 0, 1).text == '+'
    assert exp.matrix(2, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 2, 0, 2).text == '3'
    assert exp.matrix(2, 2, 0, 2).type == TokenType.RealNumber
    # exp.display2([])


def case5():
    rule = StringIO("a==(1+(2+3))")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == '=='
    assert exp.matrix(1).type == TokenType.Eq
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).text == '1'
    assert exp.matrix(2, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(2, 0, 1).text == '+'
    assert exp.matrix(2, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 2).name == 'Anonymous'
    assert exp.matrix(2, 0, 2).type == TokenType.Expression
    assert exp.matrix(2, 0, 2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 2, 0, 0).text == '2'
    assert exp.matrix(2, 0, 2, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(2, 0, 2, 0, 1).text == '+'
    assert exp.matrix(2, 0, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 2, 0, 2).text == '3'
    assert exp.matrix(2, 0, 2, 0, 2).type == TokenType.RealNumber
    # exp.display2([])


def case6():
    rule = StringIO("a==(1+(2+3)) && (1+3+4)")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == 'a'
    assert exp.matrix(0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).name == 'Anonymous'
    assert exp.matrix(0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0).text == '1'
    assert exp.matrix(0, 2, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 2, 0, 1).text == '+'
    assert exp.matrix(0, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 2, 0, 2).name == 'Anonymous'
    assert exp.matrix(0, 2, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 2, 0, 0).text == '2'
    assert exp.matrix(0, 2, 0, 2, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 2, 0, 2, 0, 1).text == '+'
    assert exp.matrix(0, 2, 0, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 2, 0, 2, 0, 2).text == '3'
    assert exp.matrix(0, 2, 0, 2, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(1).text == '&&'
    assert exp.matrix(1).type == TokenType.And
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0).text == '1'
    assert exp.matrix(2, 0, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(2, 0, 0, 1).text == '+'
    assert exp.matrix(2, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 0, 2).text == '3'
    assert exp.matrix(2, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(2, 0, 1).text == '+'
    assert exp.matrix(2, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 2).text == '4'
    assert exp.matrix(2, 0, 2).type == TokenType.RealNumber
    # exp.display2([])


def case7():
    rule = StringIO("toDate(a,b,min(c,d)+1+(data(d,e)*5))")
    exp = evals(rule)
    assert exp.name == 'toDate'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == 'b'
    assert exp.matrix(1).type == TokenType.Identifier
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).name == 'min'
    assert exp.matrix(2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0).text == 'c'
    assert exp.matrix(2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(2, 0, 0, 1).text == 'd'
    assert exp.matrix(2, 0, 0, 1).type == TokenType.Identifier
    assert exp.matrix(2, 0, 1).text == '+'
    assert exp.matrix(2, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 2).text == '1'
    assert exp.matrix(2, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(2, 1).text == '+'
    assert exp.matrix(2, 1).type == TokenType.Plus
    assert exp.matrix(2, 2).name == 'Anonymous'
    assert exp.matrix(2, 2).type == TokenType.Expression
    assert exp.matrix(2, 2, 0).name == 'Anonymous'
    assert exp.matrix(2, 2, 0).type == TokenType.Expression
    assert exp.matrix(2, 2, 0, 0).name == 'data'
    assert exp.matrix(2, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 2, 0, 0, 0).text == 'd'
    assert exp.matrix(2, 2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(2, 2, 0, 0, 1).text == 'e'
    assert exp.matrix(2, 2, 0, 0, 1).type == TokenType.Identifier
    assert exp.matrix(2, 2, 0, 1).text == '*'
    assert exp.matrix(2, 2, 0, 1).type == TokenType.Multipy
    assert exp.matrix(2, 2, 0, 2).text == '5'
    assert exp.matrix(2, 2, 0, 2).type == TokenType.RealNumber


def case8():
    rule = StringIO("toDate(a,b,min(c,d))||data(d,e)")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'toDate'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == 'a'
    assert exp.matrix(0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == 'b'
    assert exp.matrix(0, 1).type == TokenType.Identifier
    assert exp.matrix(0, 2).name == 'min'
    assert exp.matrix(0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0).text == 'c'
    assert exp.matrix(0, 2, 0).type == TokenType.Identifier
    assert exp.matrix(0, 2, 1).text == 'd'
    assert exp.matrix(0, 2, 1).type == TokenType.Identifier
    assert exp.matrix(1).text == '||'
    assert exp.matrix(1).type == TokenType.Or
    assert exp.matrix(2).name == 'data'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == 'd'
    assert exp.matrix(2, 0).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == 'e'
    assert exp.matrix(2, 1).type == TokenType.Identifier


def case9():
    rule = StringIO("(1+2)")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == '1'
    assert exp.matrix(0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 1).text == '+'
    assert exp.matrix(0, 1).type == TokenType.Plus
    assert exp.matrix(0, 2).text == '2'
    assert exp.matrix(0, 2).type == TokenType.RealNumber


def case10():
    rule = StringIO("(1+2+(3+4))")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).text == '1'
    assert exp.matrix(0, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 1).text == '+'
    assert exp.matrix(0, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 0, 2).text == '2'
    assert exp.matrix(0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 1).text == '+'
    assert exp.matrix(0, 1).type == TokenType.Plus
    assert exp.matrix(0, 2).name == 'Anonymous'
    assert exp.matrix(0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0).text == '3'
    assert exp.matrix(0, 2, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 2, 0, 1).text == '+'
    assert exp.matrix(0, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 2, 0, 2).text == '4'
    assert exp.matrix(0, 2, 0, 2).type == TokenType.RealNumber


def case11():
    rule = StringIO("toDate(a,b,min(c,d))")
    exp = evals(rule)
    assert exp.name == 'toDate'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == 'b'
    assert exp.matrix(1).type == TokenType.Identifier
    assert exp.matrix(2).name == 'min'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == 'c'
    assert exp.matrix(2, 0).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == 'd'
    assert exp.matrix(2, 1).type == TokenType.Identifier


def case12():
    rule = StringIO("a==1?true:false")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == 'a'
    assert exp.matrix(0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).text == '1'
    assert exp.matrix(0, 2).type == TokenType.RealNumber
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).text == 'true'
    assert exp.matrix(2).type == TokenType.TRUE
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'false'
    assert exp.matrix(4).type == TokenType.FALSE


def case13():
    rule = StringIO("max=a>b?a:b")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == 'max'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == '='
    assert exp.matrix(1).type == TokenType.Assignment
    assert exp.matrix(2).name == 'TernaryOperator'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).text == 'a'
    assert exp.matrix(2, 0, 0).type == TokenType.Identifier
    assert exp.matrix(2, 0, 1).text == '>'
    assert exp.matrix(2, 0, 1).type == TokenType.Gt
    assert exp.matrix(2, 0, 2).text == 'b'
    assert exp.matrix(2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == '?'
    assert exp.matrix(2, 1).type == TokenType.Question
    assert exp.matrix(2, 2).text == 'a'
    assert exp.matrix(2, 2).type == TokenType.Identifier
    assert exp.matrix(2, 3).text == ':'
    assert exp.matrix(2, 3).type == TokenType.Colon
    assert exp.matrix(2, 4).text == 'b'
    assert exp.matrix(2, 4).type == TokenType.Identifier


def case14():
    rule = StringIO("a==1?true:(x==1?y:z)")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == 'a'
    assert exp.matrix(0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).text == '1'
    assert exp.matrix(0, 2).type == TokenType.RealNumber
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).text == 'true'
    assert exp.matrix(2).type == TokenType.TRUE
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).name == 'Anonymous'
    assert exp.matrix(4).type == TokenType.Expression
    assert exp.matrix(4, 0).name == 'TernaryOperator'
    assert exp.matrix(4, 0).type == TokenType.Expression
    assert exp.matrix(4, 0, 0).name == 'Anonymous'
    assert exp.matrix(4, 0, 0).type == TokenType.Expression
    assert exp.matrix(4, 0, 0, 0).text == 'x'
    assert exp.matrix(4, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(4, 0, 0, 1).text == '=='
    assert exp.matrix(4, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(4, 0, 0, 2).text == '1'
    assert exp.matrix(4, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(4, 0, 1).text == '?'
    assert exp.matrix(4, 0, 1).type == TokenType.Question
    assert exp.matrix(4, 0, 2).text == 'y'
    assert exp.matrix(4, 0, 2).type == TokenType.Identifier
    assert exp.matrix(4, 0, 3).text == ':'
    assert exp.matrix(4, 0, 3).type == TokenType.Colon
    assert exp.matrix(4, 0, 4).text == 'z'
    assert exp.matrix(4, 0, 4).type == TokenType.Identifier
    # exp.display2([])


def case15():
    rule = StringIO("a==1?(x==1?y:z):false")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).text == 'a'
    assert exp.matrix(0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).text == '1'
    assert exp.matrix(0, 2).type == TokenType.RealNumber
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'TernaryOperator'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0).text == 'x'
    assert exp.matrix(2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(2, 0, 0, 1).text == '=='
    assert exp.matrix(2, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(2, 0, 0, 2).text == '1'
    assert exp.matrix(2, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(2, 0, 1).text == '?'
    assert exp.matrix(2, 0, 1).type == TokenType.Question
    assert exp.matrix(2, 0, 2).text == 'y'
    assert exp.matrix(2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 3).text == ':'
    assert exp.matrix(2, 0, 3).type == TokenType.Colon
    assert exp.matrix(2, 0, 4).text == 'z'
    assert exp.matrix(2, 0, 4).type == TokenType.Identifier
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'false'
    assert exp.matrix(4).type == TokenType.FALSE

    # exp.display2([])


def case16():
    rule = StringIO("taDate(a==1?(x==1?y:z):false,a)")
    exp = evals(rule)
    assert exp.name == 'taDate'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'TernaryOperator'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).text == 'a'
    assert exp.matrix(0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 0, 1).text == '=='
    assert exp.matrix(0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 2).text == '1'
    assert exp.matrix(0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 1).text == '?'
    assert exp.matrix(0, 1).type == TokenType.Question
    assert exp.matrix(0, 2).name == 'Anonymous'
    assert exp.matrix(0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0).name == 'TernaryOperator'
    assert exp.matrix(0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0, 0).text == 'x'
    assert exp.matrix(0, 2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 2, 0, 0, 1).text == '=='
    assert exp.matrix(0, 2, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2, 0, 0, 2).text == '1'
    assert exp.matrix(0, 2, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 2, 0, 1).text == '?'
    assert exp.matrix(0, 2, 0, 1).type == TokenType.Question
    assert exp.matrix(0, 2, 0, 2).text == 'y'
    assert exp.matrix(0, 2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 2, 0, 3).text == ':'
    assert exp.matrix(0, 2, 0, 3).type == TokenType.Colon
    assert exp.matrix(0, 2, 0, 4).text == 'z'
    assert exp.matrix(0, 2, 0, 4).type == TokenType.Identifier
    assert exp.matrix(0, 3).text == ':'
    assert exp.matrix(0, 3).type == TokenType.Colon
    assert exp.matrix(0, 4).text == 'false'
    assert exp.matrix(0, 4).type == TokenType.FALSE
    assert exp.matrix(1).text == 'a'
    assert exp.matrix(1).type == TokenType.Identifier


def case17():
    rule = StringIO("taDate(a==1?(x==1?y:z):false, abc(1+2))==1?a+b+c:true")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'taDate'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'TernaryOperator'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0).text == 'a'
    assert exp.matrix(0, 0, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 0, 1).text == '=='
    assert exp.matrix(0, 0, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 0, 0, 2).text == '1'
    assert exp.matrix(0, 0, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 0, 1).text == '?'
    assert exp.matrix(0, 0, 0, 1).type == TokenType.Question
    assert exp.matrix(0, 0, 0, 2).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 2, 0).name == 'TernaryOperator'
    assert exp.matrix(0, 0, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 2, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 2, 0, 0, 0).text == 'x'
    assert exp.matrix(0, 0, 0, 2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 2, 0, 0, 1).text == '=='
    assert exp.matrix(0, 0, 0, 2, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 0, 2, 0, 0, 2).text == '1'
    assert exp.matrix(0, 0, 0, 2, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 0, 2, 0, 1).text == '?'
    assert exp.matrix(0, 0, 0, 2, 0, 1).type == TokenType.Question
    assert exp.matrix(0, 0, 0, 2, 0, 2).text == 'y'
    assert exp.matrix(0, 0, 0, 2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 2, 0, 3).text == ':'
    assert exp.matrix(0, 0, 0, 2, 0, 3).type == TokenType.Colon
    assert exp.matrix(0, 0, 0, 2, 0, 4).text == 'z'
    assert exp.matrix(0, 0, 0, 2, 0, 4).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 3).text == ':'
    assert exp.matrix(0, 0, 0, 3).type == TokenType.Colon
    assert exp.matrix(0, 0, 0, 4).text == 'false'
    assert exp.matrix(0, 0, 0, 4).type == TokenType.FALSE
    assert exp.matrix(0, 0, 1).name == 'abc'
    assert exp.matrix(0, 0, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 1, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0, 0).text == '1'
    assert exp.matrix(0, 0, 1, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 1, 0, 1).text == '+'
    assert exp.matrix(0, 0, 1, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 0, 1, 0, 2).text == '2'
    assert exp.matrix(0, 0, 1, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).text == '1'
    assert exp.matrix(0, 2).type == TokenType.RealNumber
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).text == 'a'
    assert exp.matrix(2, 0, 0).type == TokenType.Identifier
    assert exp.matrix(2, 0, 1).text == '+'
    assert exp.matrix(2, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 2).text == 'b'
    assert exp.matrix(2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == '+'
    assert exp.matrix(2, 1).type == TokenType.Plus
    assert exp.matrix(2, 2).text == 'c'
    assert exp.matrix(2, 2).type == TokenType.Identifier
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE

    # exp.display2([])


def case18():
    rule = StringIO(
        """toDate($C1D1.ONC-392 Administration.ECSTDAT)!=""&& toDate($*.*.LBDAT)!=""&& toDate("2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00")!="" &&toDate("2015-1-12 "+$*.*.*+":00")!=""?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0:true""")
    exp = evals(rule)

    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 0).name == 'toDate'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 0, 0).text == '$C1D1.ONC-392 Administration.ECSTDAT'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 2).text == '""'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 0, 0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 0, 0, 0, 0, 2).name == 'toDate'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0, 2, 0).text == '$*.*.LBDAT'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 2, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 0, 0, 2).text == '""'
    assert exp.matrix(0, 0, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 0, 0, 2).name == 'toDate'
    assert exp.matrix(0, 0, 0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0, 0).text == '"2015-1-12 "'
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0, 1).text == '+'
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0, 2).text == '$C1D1.ONC-392 Administration.ECSTTIM'
    assert exp.matrix(0, 0, 0, 0, 2, 0, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 0, 2, 0, 1).text == '+'
    assert exp.matrix(0, 0, 0, 0, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 0, 0, 0, 2, 0, 2).text == '":00"'
    assert exp.matrix(0, 0, 0, 0, 2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 2).text == '""'
    assert exp.matrix(0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 2).name == 'toDate'
    assert exp.matrix(0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 0, 0).text == '"2015-1-12 "'
    assert exp.matrix(0, 0, 2, 0, 0, 0).type == TokenType.Identifier
    assert exp.matrix(0, 0, 2, 0, 0, 1).text == '+'
    assert exp.matrix(0, 0, 2, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 0, 2, 0, 0, 2).text == '$*.*.*'
    assert exp.matrix(0, 0, 2, 0, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 0, 2, 0, 1).text == '+'
    assert exp.matrix(0, 0, 2, 0, 1).type == TokenType.Plus
    assert exp.matrix(0, 0, 2, 0, 2).text == '":00"'
    assert exp.matrix(0, 0, 2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == '!='
    assert exp.matrix(0, 1).type == TokenType.NEq
    assert exp.matrix(0, 2).text == '""'
    assert exp.matrix(0, 2).type == TokenType.Identifier
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'dateDiff'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0, 0, 0).text == '$C1D1.ONC-392 Administration.ECSTDAT'
    assert exp.matrix(2, 0, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(2, 0, 0, 0, 0, 1).text == '+'
    assert exp.matrix(2, 0, 0, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 0, 0, 0, 2).text == '" "'
    assert exp.matrix(2, 0, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 0, 0, 1).text == '+'
    assert exp.matrix(2, 0, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 0, 0, 2).text == '$C1D1.ONC-392 Administration.ECSTTIM'
    assert exp.matrix(2, 0, 0, 0, 2).type == TokenType.Variable
    assert exp.matrix(2, 0, 0, 1).text == '+'
    assert exp.matrix(2, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 0, 2).text == '":00"'
    assert exp.matrix(2, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 1).name == 'Anonymous'
    assert exp.matrix(2, 0, 1).type == TokenType.Expression
    assert exp.matrix(2, 0, 1, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 1, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 1, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 1, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 1, 0, 0, 0).text == '$*.*.LBDAT'
    assert exp.matrix(2, 0, 1, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(2, 0, 1, 0, 0, 1).text == '+'
    assert exp.matrix(2, 0, 1, 0, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 1, 0, 0, 2).text == '" "'
    assert exp.matrix(2, 0, 1, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 1, 0, 1).text == '+'
    assert exp.matrix(2, 0, 1, 0, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 1, 0, 2).text == '$*.*.*'
    assert exp.matrix(2, 0, 1, 0, 2).type == TokenType.Variable
    assert exp.matrix(2, 0, 1, 1).text == '+'
    assert exp.matrix(2, 0, 1, 1).type == TokenType.Plus
    assert exp.matrix(2, 0, 1, 2).text == '":00"'
    assert exp.matrix(2, 0, 1, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 2).text == '"m"'
    assert exp.matrix(2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == '>'
    assert exp.matrix(2, 1).type == TokenType.Gt
    assert exp.matrix(2, 2).text == '0'
    assert exp.matrix(2, 2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE
    # exp.display2([])


def case19():
    rule = StringIO(
        """autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01), true)""")
    exp = evals(rule)

    assert exp.name == 'autoValue'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'RoundN'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'sum'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'getSumOfItemInLog'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLLONG'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 1).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 1, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 1, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 1, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 1, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 1, 0, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert exp.matrix(0, 0, 0, 1, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 1, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 1, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 1, 0, 0, 2).text == '11'
    assert exp.matrix(0, 0, 0, 1, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 0, 1, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 0, 1, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 0, 1, 0, 2).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU '
    assert exp.matrix(0, 0, 0, 1, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 1, 1).text == '=='
    assert exp.matrix(0, 0, 0, 1, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 0, 1, 2).text == '"CM"'
    assert exp.matrix(0, 0, 0, 1, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 1).name == 'multiply'
    assert exp.matrix(0, 0, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0).name == 'getSumOfItemInLog'
    assert exp.matrix(0, 0, 1, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLLONG'
    assert exp.matrix(0, 0, 1, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 1, 0, 1).name == 'Anonymous'
    assert exp.matrix(0, 0, 1, 0, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0, 1, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 1, 0, 1, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0, 2).text == '11'
    assert exp.matrix(0, 0, 1, 0, 1, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 1, 0, 1, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 1, 0, 1, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 1, 0, 1, 0, 2).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU '
    assert exp.matrix(0, 0, 1, 0, 1, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 0, 1, 0, 1, 1).text == '=='
    assert exp.matrix(0, 0, 1, 0, 1, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 1, 0, 1, 2).text == '"MM"'
    assert exp.matrix(0, 0, 1, 0, 1, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 1, 1).name == 'Anonymous'
    assert exp.matrix(0, 0, 1, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 1, 1, 0).text == '1'
    assert exp.matrix(0, 0, 1, 1, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 1, 1, 1).text == '/'
    assert exp.matrix(0, 0, 1, 1, 1).type == TokenType.Divide
    assert exp.matrix(0, 0, 1, 1, 2).text == '10'
    assert exp.matrix(0, 0, 1, 1, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 2).name == 'getSumOfItemInLog'
    assert exp.matrix(0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLSHORT'
    assert exp.matrix(0, 0, 2, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 2, 1).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 1, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 1, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 1, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 1, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 1, 0, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert exp.matrix(0, 0, 2, 1, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 2, 1, 0, 0, 1).text == '=='
    assert exp.matrix(0, 0, 2, 1, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 2, 1, 0, 0, 2).text == '11'
    assert exp.matrix(0, 0, 2, 1, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 2, 1, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 2, 1, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 2, 1, 0, 2).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU'
    assert exp.matrix(0, 0, 2, 1, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 0, 2, 1, 1).text == '=='
    assert exp.matrix(0, 0, 2, 1, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 2, 1, 2).text == '"CM"'
    assert exp.matrix(0, 0, 2, 1, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 3).name == 'multiply'
    assert exp.matrix(0, 0, 3).type == TokenType.Expression
    assert exp.matrix(0, 0, 3, 0).name == 'getSumOfItemInLog'
    assert exp.matrix(0, 0, 3, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 3, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLSHORT'
    assert exp.matrix(0, 0, 3, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 3, 0, 1).name == 'Anonymous'
    assert exp.matrix(0, 0, 3, 0, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 3, 0, 1, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 3, 0, 1, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0, 0).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0, 1).text == '=='
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0, 2).text == '11'
    assert exp.matrix(0, 0, 3, 0, 1, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 3, 0, 1, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 3, 0, 1, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 3, 0, 1, 0, 2).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU'
    assert exp.matrix(0, 0, 3, 0, 1, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 0, 3, 0, 1, 1).text == '=='
    assert exp.matrix(0, 0, 3, 0, 1, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 3, 0, 1, 2).text == '"MM"'
    assert exp.matrix(0, 0, 3, 0, 1, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 3, 1).name == 'Anonymous'
    assert exp.matrix(0, 0, 3, 1).type == TokenType.Expression
    assert exp.matrix(0, 0, 3, 1, 0).text == '1'
    assert exp.matrix(0, 0, 3, 1, 0).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 3, 1, 1).text == '/'
    assert exp.matrix(0, 0, 3, 1, 1).type == TokenType.Divide
    assert exp.matrix(0, 0, 3, 1, 2).text == '10'
    assert exp.matrix(0, 0, 3, 1, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 1).text == '0.01'
    assert exp.matrix(0, 1).type == TokenType.RealNumber
    assert exp.matrix(1).text == 'true'
    assert exp.matrix(1).type == TokenType.TRUE


def case20():
    rule = StringIO(
        """mustAnswer($*.*.*)&&(getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)=='V1.5'||getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)=='V1.6')?($*.*.*=='0'||$*.*.*=='1'||$*.*.*=='2'):true""")
    exp = evals(rule)

    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'mustAnswer'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).text == '$*.*.*'
    assert exp.matrix(0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 1).text == '&&'
    assert exp.matrix(0, 1).type == TokenType.And
    assert exp.matrix(0, 2).name == 'Anonymous'
    assert exp.matrix(0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 2, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0, 0, 0).name == 'getICFVersion'
    assert exp.matrix(0, 2, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0, 0, 0, 0).text == '$*.Date of Visit.SVDAT'
    assert exp.matrix(0, 2, 0, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 2, 0, 0, 0, 0, 1).text == '$*.Informed Consent.DSSTDAT'
    assert exp.matrix(0, 2, 0, 0, 0, 0, 1).type == TokenType.Variable
    assert exp.matrix(0, 2, 0, 0, 0, 0, 2).text == '$*.Informed Consent.VERSION'
    assert exp.matrix(0, 2, 0, 0, 0, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 2, 0, 0, 0, 1).text == '=='
    assert exp.matrix(0, 2, 0, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2, 0, 0, 0, 2).text == '\'V1.5\''
    assert exp.matrix(0, 2, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 2, 0, 0, 1).text == '||'
    assert exp.matrix(0, 2, 0, 0, 1).type == TokenType.Or
    assert exp.matrix(0, 2, 0, 0, 2).name == 'getICFVersion'
    assert exp.matrix(0, 2, 0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0, 0, 2, 0).text == '$*.Date of Visit.SVDAT'
    assert exp.matrix(0, 2, 0, 0, 2, 0).type == TokenType.Variable
    assert exp.matrix(0, 2, 0, 0, 2, 1).text == '$*.Informed Consent.DSSTDAT'
    assert exp.matrix(0, 2, 0, 0, 2, 1).type == TokenType.Variable
    assert exp.matrix(0, 2, 0, 0, 2, 2).text == '$*.Informed Consent.VERSION'
    assert exp.matrix(0, 2, 0, 0, 2, 2).type == TokenType.Variable
    assert exp.matrix(0, 2, 0, 1).text == '=='
    assert exp.matrix(0, 2, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2, 0, 2).text == '\'V1.6\''
    assert exp.matrix(0, 2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'Anonymous'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(2, 0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0, 0, 0, 0).text == '$*.*.*'
    assert exp.matrix(2, 0, 0, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(2, 0, 0, 0, 0, 0, 1).text == '=='
    assert exp.matrix(2, 0, 0, 0, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(2, 0, 0, 0, 0, 0, 2).text == '\'0\''
    assert exp.matrix(2, 0, 0, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 0, 0, 0, 1).text == '||'
    assert exp.matrix(2, 0, 0, 0, 0, 1).type == TokenType.Or
    assert exp.matrix(2, 0, 0, 0, 0, 2).text == '$*.*.*'
    assert exp.matrix(2, 0, 0, 0, 0, 2).type == TokenType.Variable
    assert exp.matrix(2, 0, 0, 0, 1).text == '=='
    assert exp.matrix(2, 0, 0, 0, 1).type == TokenType.Eq
    assert exp.matrix(2, 0, 0, 0, 2).text == '\'1\''
    assert exp.matrix(2, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 0, 0, 1).text == '||'
    assert exp.matrix(2, 0, 0, 1).type == TokenType.Or
    assert exp.matrix(2, 0, 0, 2).text == '$*.*.*'
    assert exp.matrix(2, 0, 0, 2).type == TokenType.Variable
    assert exp.matrix(2, 0, 1).text == '=='
    assert exp.matrix(2, 0, 1).type == TokenType.Eq
    assert exp.matrix(2, 0, 2).text == '\'2\''
    assert exp.matrix(2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE


def case21():
    rule = StringIO(
        """toDate($*.*.*)!=""&&toDate(getMinByLog($*.Informed Consent.DSSTDAT))!=""?dateDiff(getMinByLog($*.Informed Consent.DSSTDAT),$*.*.*, "D")>0:true""")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).name == 'toDate'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0).text == '$*.*.*'
    assert exp.matrix(0, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 2).text == '""'
    assert exp.matrix(0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 2).name == 'toDate'
    assert exp.matrix(0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0).name == 'getMinByLog'
    assert exp.matrix(0, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 0).text == '$*.Informed Consent.DSSTDAT'
    assert exp.matrix(0, 0, 2, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 1).text == '!='
    assert exp.matrix(0, 1).type == TokenType.NEq
    assert exp.matrix(0, 2).text == '""'
    assert exp.matrix(0, 2).type == TokenType.Identifier
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'dateDiff'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).name == 'getMinByLog'
    assert exp.matrix(2, 0, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0, 0).text == '$*.Informed Consent.DSSTDAT'
    assert exp.matrix(2, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(2, 0, 1).text == '$*.*.*'
    assert exp.matrix(2, 0, 1).type == TokenType.Variable
    assert exp.matrix(2, 0, 2).text == '"D"'
    assert exp.matrix(2, 0, 2).type == TokenType.Identifier
    assert exp.matrix(2, 1).text == '>'
    assert exp.matrix(2, 1).type == TokenType.Gt
    assert exp.matrix(2, 2).text == '0'
    assert exp.matrix(2, 2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE


def case22():
    rule = StringIO("""isValidDate($*.*.*)""")
    exp = evals(rule)
    assert exp.name == 'isValidDate'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == '$*.*.*'
    assert exp.matrix(0).type == TokenType.Variable


def case23():
    rule = StringIO(
        """autoValue((toNum($*.*.EGORRES.881)!=''&&toNum($*.*.EGORRES.879)!=''?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), "1"):""), true)""")
    exp = evals(rule)
    assert exp.name == 'autoValue'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'TernaryOperator'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0).name == 'toNum'
    assert exp.matrix(0, 0, 0, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0).text == '$*.*.EGORRES.881'
    assert exp.matrix(0, 0, 0, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 0, 0, 2).text == '\'\''
    assert exp.matrix(0, 0, 0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 0, 0, 2).name == 'toNum'
    assert exp.matrix(0, 0, 0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0, 2, 0).text == '$*.*.EGORRES.879'
    assert exp.matrix(0, 0, 0, 0, 2, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 0, 1).text == '!='
    assert exp.matrix(0, 0, 0, 1).type == TokenType.NEq
    assert exp.matrix(0, 0, 0, 2).text == '\'\''
    assert exp.matrix(0, 0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 0, 1).text == '?'
    assert exp.matrix(0, 0, 1).type == TokenType.Question
    assert exp.matrix(0, 0, 2).name == 'RoundN'
    assert exp.matrix(0, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 0).name == 'toNum'
    assert exp.matrix(0, 0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 0, 0).text == '$*.*.EGORRES.879'
    assert exp.matrix(0, 0, 2, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 2, 0, 1).text == '/'
    assert exp.matrix(0, 0, 2, 0, 1).type == TokenType.Divide
    assert exp.matrix(0, 0, 2, 0, 2).name == 'Math.pow'
    assert exp.matrix(0, 0, 2, 0, 2).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 2, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 0, 2, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 0).name == 'toNum'
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 0, 0).text == '$*.*.EGORRES.881'
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 1).text == '/'
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 1).type == TokenType.Divide
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 2).text == '1000'
    assert exp.matrix(0, 0, 2, 0, 2, 0, 0, 2).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 2, 0, 2, 1).text == '0.33'
    assert exp.matrix(0, 0, 2, 0, 2, 1).type == TokenType.RealNumber
    assert exp.matrix(0, 0, 2, 1).text == '"1"'
    assert exp.matrix(0, 0, 2, 1).type == TokenType.Identifier
    assert exp.matrix(0, 0, 3).text == ':'
    assert exp.matrix(0, 0, 3).type == TokenType.Colon
    assert exp.matrix(0, 0, 4).text == '""'
    assert exp.matrix(0, 0, 4).type == TokenType.Identifier
    assert exp.matrix(1).text == 'true'
    assert exp.matrix(1).type == TokenType.TRUE


def case24():
    rule = StringIO("$*.*.EGPERF==\"Y\"")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == '$*.*.EGPERF'
    assert exp.matrix(0).type == TokenType.Variable
    assert exp.matrix(1).text == '=='
    assert exp.matrix(1).type == TokenType.Eq
    assert exp.matrix(2).text == '"Y"'
    assert exp.matrix(2).type == TokenType.Identifier


def case25():
    rule = StringIO("$*.*.EGORRES.12394==\"CS\"")
    exp = evals(rule)
    assert exp.name == 'Anonymous'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == '$*.*.EGORRES.12394'
    assert exp.matrix(0).type == TokenType.Variable
    assert exp.matrix(1).text == '=='
    assert exp.matrix(1).type == TokenType.Eq
    assert exp.matrix(2).text == '"CS"'
    assert exp.matrix(2).type == TokenType.Identifier


def case26():
    rule = StringIO("""condition(mustAnswer(toNum($*.*.*)), isRange($*.*.*, 40,160))""")
    exp = evals(rule)
    assert exp.name == 'condition'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'mustAnswer'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'toNum'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).text == '$*.*.*'
    assert exp.matrix(0, 0, 0).type == TokenType.Variable
    assert exp.matrix(1).name == 'isRange'
    assert exp.matrix(1).type == TokenType.Expression
    assert exp.matrix(1, 0).text == '$*.*.*'
    assert exp.matrix(1, 0).type == TokenType.Variable
    assert exp.matrix(1, 1).text == '40'
    assert exp.matrix(1, 1).type == TokenType.RealNumber
    assert exp.matrix(1, 2).text == '160'
    assert exp.matrix(1, 2).type == TokenType.RealNumber


def case27():
    rule = StringIO("""mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='Y'?$*.*.*=='':true""")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'mustAnswer'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).text == '$*.*.CRONGO'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 2).text == '$*.*.CRONGO'
    assert exp.matrix(0, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).text == '\'Y\''
    assert exp.matrix(0, 2).type == TokenType.Identifier
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == '$*.*.*'
    assert exp.matrix(2, 0).type == TokenType.Variable
    assert exp.matrix(2, 1).text == '=='
    assert exp.matrix(2, 1).type == TokenType.Eq
    assert exp.matrix(2, 2).text == '\'\''
    assert exp.matrix(2, 2).type == TokenType.Identifier
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE


def case28():
    rule = StringIO("mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'?$*.*.*!='':true")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).name == 'mustAnswer'
    assert exp.matrix(0, 0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0, 0).text == '$*.*.CRONGO'
    assert exp.matrix(0, 0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 1).text == '&&'
    assert exp.matrix(0, 0, 1).type == TokenType.And
    assert exp.matrix(0, 0, 2).text == '$*.*.CRONGO'
    assert exp.matrix(0, 0, 2).type == TokenType.Variable
    assert exp.matrix(0, 1).text == '=='
    assert exp.matrix(0, 1).type == TokenType.Eq
    assert exp.matrix(0, 2).text == '\'N\''
    assert exp.matrix(0, 2).type == TokenType.Identifier
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).text == '$*.*.*'
    assert exp.matrix(2, 0).type == TokenType.Variable
    assert exp.matrix(2, 1).text == '!='
    assert exp.matrix(2, 1).type == TokenType.NEq
    assert exp.matrix(2, 2).text == '\'\''
    assert exp.matrix(2, 2).type == TokenType.Identifier
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE


def case29():
    rule = StringIO("""autoIncrease(1,1,1,1)""")
    exp = evals(rule)
    assert exp.name == 'autoIncrease'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).text == '1'
    assert exp.matrix(0).type == TokenType.RealNumber
    assert exp.matrix(1).text == '1'
    assert exp.matrix(1).type == TokenType.RealNumber
    assert exp.matrix(2).text == '1'
    assert exp.matrix(2).type == TokenType.RealNumber
    assert exp.matrix(3).text == '1'
    assert exp.matrix(3).type == TokenType.RealNumber


def case30():
    rule = StringIO("""$*.*.*=='Y'&&mustAnswer($*.Demographics.AGE)?toNum($*.Demographics.AGE)>=18:true""")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.type == TokenType.Expression
    assert exp.matrix(0).name == 'Anonymous'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'Anonymous'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(0, 0, 0).text == '$*.*.*'
    assert exp.matrix(0, 0, 0).type == TokenType.Variable
    assert exp.matrix(0, 0, 1).text == '=='
    assert exp.matrix(0, 0, 1).type == TokenType.Eq
    assert exp.matrix(0, 0, 2).text == '\'Y\''
    assert exp.matrix(0, 0, 2).type == TokenType.Identifier
    assert exp.matrix(0, 1).text == '&&'
    assert exp.matrix(0, 1).type == TokenType.And
    assert exp.matrix(0, 2).name == 'mustAnswer'
    assert exp.matrix(0, 2).type == TokenType.Expression
    assert exp.matrix(0, 2, 0).text == '$*.Demographics.AGE'
    assert exp.matrix(0, 2, 0).type == TokenType.Variable
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).name == 'Anonymous'
    assert exp.matrix(2).type == TokenType.Expression
    assert exp.matrix(2, 0).name == 'toNum'
    assert exp.matrix(2, 0).type == TokenType.Expression
    assert exp.matrix(2, 0, 0).text == '$*.Demographics.AGE'
    assert exp.matrix(2, 0, 0).type == TokenType.Variable
    assert exp.matrix(2, 1).text == '>='
    assert exp.matrix(2, 1).type == TokenType.Ge
    assert exp.matrix(2, 2).text == '18'
    assert exp.matrix(2, 2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == 'true'
    assert exp.matrix(4).type == TokenType.TRUE


def case31():
    rule = StringIO("""a?1:2""")
    exp = evals(rule)
    assert exp.name == 'TernaryOperator'
    assert exp.matrix(0).text == 'a'
    assert exp.matrix(0).type == TokenType.Identifier
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).text == '1'
    assert exp.matrix(2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).text == '2'
    assert exp.matrix(4).type == TokenType.RealNumber


def case32():
    rule = StringIO("a()")
    exp = evals(rule)
    assert exp.name == 'a'
    assert exp.type == TokenType.Expression
    assert len(exp.body) == 0


def case33():
    rule = StringIO("""a()?1:b()""")
    exp = evals(rule)
    exp.display2([])
    assert exp.name == 'TernaryOperator'
    assert exp.matrix(0).name == 'a'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).text == '1'
    assert exp.matrix(2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).name == 'b'
    assert exp.matrix(4).type == TokenType.Expression

def case34():
    rule = StringIO("""a(c())?1:b(d())""")
    exp = evals(rule)
    exp.display2([])
    assert exp.name == "TernaryOperator"
    assert exp.matrix(0).name == 'a'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'c'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).text == '1'
    assert exp.matrix(2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).name == 'b'
    assert exp.matrix(4).type == TokenType.Expression
    assert exp.matrix(4, 0).name == 'd'
    assert exp.matrix(4, 0).type == TokenType.Expression
    # print(exp)


def case35():
    rule = StringIO("a(c())?1:b(d(1,2),x())")
    exp = evals(rule)
    assert exp.name == "TernaryOperator"
    assert exp.matrix(0).name == 'a'
    assert exp.matrix(0).type == TokenType.Expression
    assert exp.matrix(0, 0).name == 'c'
    assert exp.matrix(0, 0).type == TokenType.Expression
    assert exp.matrix(1).text == '?'
    assert exp.matrix(1).type == TokenType.Question
    assert exp.matrix(2).text == '1'
    assert exp.matrix(2).type == TokenType.RealNumber
    assert exp.matrix(3).text == ':'
    assert exp.matrix(3).type == TokenType.Colon
    assert exp.matrix(4).name == 'b'
    assert exp.matrix(4).type == TokenType.Expression
    assert exp.matrix(4, 0).name == 'd'
    assert exp.matrix(4, 0).type == TokenType.Expression
    assert exp.matrix(4, 0, 0).text == '1'
    assert exp.matrix(4, 0, 0).type == TokenType.RealNumber
    assert exp.matrix(4, 0, 1).text == '2'
    assert exp.matrix(4, 0, 1).type == TokenType.RealNumber
    assert exp.matrix(4, 1).name == 'x'
    assert exp.matrix(4, 1).type == TokenType.Expression

def test_interpreter2():
    case35()


def test_interpreter():
    case0()
    case1()
    case2()
    case3()
    case4()
    case5()
    case6()
    case7()
    case8()
    case9()
    case10()
    case11()
    case12()
    case13()
    case14()
    case15()
    case16()
    case17()
    case18()
    case19()
    case20()
    case21()
    case22()
    case23()
    case24()
    case25()
    case26()
    case27()
    case28()
    case29()
    case30()
    case31()
    case32()
    case33()
    case34()
    case35()