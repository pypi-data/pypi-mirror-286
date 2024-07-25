from io import StringIO

from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.token_type import TokenType
from edkrule.interpreter.parse.parser import Parser


def case1():
    s = StringIO("a(1+2+b(2))")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'a'
    # assert es.statement.content[0].content[0].text == 'a'
    # assert es.statement.content[0].content[1].text == '('
    assert es.statement.matrix(0, 1).text == '('
    # assert es.statement.content[0].content[2].content[0].content[0].text == '1'
    assert es.statement.matrix(0, 2, 0, 0).text == '1'
    assert es.statement.body[0].body[2].body[1].text == '+'
    assert es.statement.body[0].body[2].body[2].body[0].text == '2'
    assert es.statement.body[0].body[2].body[3].text == '+'
    assert es.statement.body[0].body[2].body[4].body[0].text == 'b'
    assert es.statement.body[0].body[2].body[4].body[1].text == '('
    assert es.statement.body[0].body[2].body[4].body[2].body[0].text == '2'
    assert es.statement.body[0].body[2].body[4].body[3].text == ')'
    assert es.statement.body[0].body[3].text == ')'
    assert es.statement.text == s.getvalue()


def case2():
    s = StringIO("b(2,3+1,4)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.body[0].body[0].text == 'b'
    assert es.statement.body[0].body[0].type == TokenType.Identifier
    assert es.statement.body[0].body[1].text == '('
    assert es.statement.body[0].body[1].type == TokenType.Lp
    assert es.statement.body[0].body[2].body[0].text == '2'
    assert es.statement.body[0].body[2].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[3].text == ','
    assert es.statement.body[0].body[3].type == TokenType.Comma
    assert es.statement.body[0].body[4].body[0].text == '3'
    assert es.statement.body[0].body[4].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[4].body[1].text == '+'
    assert es.statement.body[0].body[4].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[4].body[2].text == '1'
    assert es.statement.body[0].body[4].body[2].type == TokenType.RealNumber
    assert es.statement.body[0].body[5].text == ','
    assert es.statement.body[0].body[5].type == TokenType.Comma
    assert es.statement.body[0].body[6].body[0].text == '4'
    assert es.statement.body[0].body[6].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[7].text == ')'
    assert es.statement.body[0].body[7].type == TokenType.Rp

    assert es.statement.text == s.getvalue()


def case3():
    s = StringIO("date((1+2)+3==(4+5), year(\"xxxx\"), 9+10)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.body[0].body[0].text == 'date'
    assert es.statement.body[0].body[0].type == TokenType.Identifier
    assert es.statement.body[0].body[1].text == '('
    assert es.statement.body[0].body[1].type == TokenType.Lp
    assert es.statement.body[0].body[2].body[0].body[0].text == '('
    assert es.statement.body[0].body[2].body[0].body[0].type == TokenType.Lp
    assert es.statement.body[0].body[2].body[0].body[1].body[0].text == '1'
    assert es.statement.body[0].body[2].body[0].body[1].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[0].body[1].body[1].text == '+'
    assert es.statement.body[0].body[2].body[0].body[1].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[0].body[1].body[2].text == '2'
    assert es.statement.body[0].body[2].body[0].body[1].body[2].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[0].body[2].text == ')'
    assert es.statement.body[0].body[2].body[0].body[2].type == TokenType.Rp
    assert es.statement.body[0].body[2].body[1].text == '+'
    assert es.statement.body[0].body[2].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[2].text == '3'
    assert es.statement.body[0].body[2].body[2].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[3].text == '=='
    assert es.statement.body[0].body[2].body[3].type == TokenType.Eq
    assert es.statement.body[0].body[2].body[4].body[0].text == '('
    assert es.statement.body[0].body[2].body[4].body[0].type == TokenType.Lp
    assert es.statement.body[0].body[2].body[4].body[1].body[0].text == '4'
    assert es.statement.body[0].body[2].body[4].body[1].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[4].body[1].body[1].text == '+'
    assert es.statement.body[0].body[2].body[4].body[1].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[4].body[1].body[2].text == '5'
    assert es.statement.body[0].body[2].body[4].body[1].body[2].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[4].body[2].text == ')'
    assert es.statement.body[0].body[2].body[4].body[2].type == TokenType.Rp

    assert es.statement.body[0].body[3].text == ','
    assert es.statement.body[0].body[3].type == TokenType.Comma
    assert es.statement.body[0].body[4].body[0].text == ' '
    assert es.statement.body[0].body[4].body[0].type == TokenType.Blank
    assert es.statement.body[0].body[4].body[1].body[0].text == 'year'
    assert es.statement.body[0].body[4].body[1].body[0].type == TokenType.Identifier
    assert es.statement.body[0].body[4].body[1].body[1].text == '('
    assert es.statement.body[0].body[4].body[1].body[1].type == TokenType.Lp
    assert es.statement.body[0].body[4].body[1].body[2].text == '"xxxx"'
    assert es.statement.body[0].body[4].body[1].body[2].type == TokenType.Identifier
    assert es.statement.body[0].body[4].body[1].body[3].text == ')'
    assert es.statement.body[0].body[4].body[1].body[3].type == TokenType.Rp
    assert es.statement.body[0].body[5].text == ','
    assert es.statement.body[0].body[5].type == TokenType.Comma
    assert es.statement.body[0].body[6].body[0].text == ' '
    assert es.statement.body[0].body[6].body[0].type == TokenType.Blank
    assert es.statement.body[0].body[6].body[1].text == '9'
    assert es.statement.body[0].body[6].body[1].type == TokenType.RealNumber
    assert es.statement.body[0].body[6].body[2].text == '+'
    assert es.statement.body[0].body[6].body[2].type == TokenType.Plus
    assert es.statement.body[0].body[6].body[3].text == '10'
    assert es.statement.body[0].body[6].body[3].type == TokenType.RealNumber
    assert es.statement.body[0].body[7].text == ')'
    assert es.statement.body[0].body[7].type == TokenType.Rp

    assert es.statement.text == s.getvalue()


def case4():
    s = StringIO("a+b==1?2+3:4+1+2")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.body[0].text == 'a'
    assert es.statement.body[0].type == TokenType.Identifier

    assert es.statement.body[1].text == '+'
    assert es.statement.body[1].type == TokenType.Plus

    assert es.statement.body[2].text == 'b'
    assert es.statement.body[2].type == TokenType.Identifier

    assert es.statement.body[3].text == '=='
    assert es.statement.body[3].type == TokenType.Eq

    assert es.statement.body[4].text == '1'
    assert es.statement.body[4].type == TokenType.RealNumber

    assert es.statement.body[5].text == "?"
    assert es.statement.body[5].type == TokenType.Question

    assert es.statement.body[6].body[0].text == '2'
    assert es.statement.body[6].body[0].type == TokenType.RealNumber
    assert es.statement.body[6].body[1].text == '+'
    assert es.statement.body[6].body[1].type == TokenType.Plus
    assert es.statement.body[6].body[2].text == '3'
    assert es.statement.body[6].body[2].type == TokenType.RealNumber

    assert es.statement.body[7].text == ':'
    assert es.statement.body[7].type == TokenType.Colon

    assert es.statement.body[8].body[0].text == '4'
    assert es.statement.body[8].body[0].type == TokenType.RealNumber
    assert es.statement.body[8].body[1].text == '+'
    assert es.statement.body[8].body[1].type == TokenType.Plus
    assert es.statement.body[8].body[2].text == '1'
    assert es.statement.body[8].body[2].type == TokenType.RealNumber
    assert es.statement.body[8].body[3].text == '+'
    assert es.statement.body[8].body[3].type == TokenType.Plus
    assert es.statement.body[8].body[4].text == '2'
    assert es.statement.body[8].body[4].type == TokenType.RealNumber

    assert es.statement.text == s.getvalue()


def case5():
    s = StringIO("taDate(a+b==1?2+3:4+1+2,111)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.body[0].body[0].text == 'taDate'
    assert es.statement.body[0].body[0].type == TokenType.Identifier
    assert es.statement.body[0].body[1].text == '('
    assert es.statement.body[0].body[1].type == TokenType.Lp
    assert es.statement.body[0].body[2].body[0].text == 'a'
    assert es.statement.body[0].body[2].body[0].type == TokenType.Identifier
    assert es.statement.body[0].body[2].body[1].text == '+'
    assert es.statement.body[0].body[2].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[2].text == 'b'
    assert es.statement.body[0].body[2].body[2].type == TokenType.Identifier
    assert es.statement.body[0].body[2].body[3].text == '=='
    assert es.statement.body[0].body[2].body[3].type == TokenType.Eq
    assert es.statement.body[0].body[2].body[4].text == '1'
    assert es.statement.body[0].body[2].body[4].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[5].text == '?'
    assert es.statement.body[0].body[2].body[5].type == TokenType.Question
    assert es.statement.body[0].body[2].body[6].body[0].text == '2'
    assert es.statement.body[0].body[2].body[6].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[6].body[1].text == '+'
    assert es.statement.body[0].body[2].body[6].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[6].body[2].text == '3'
    assert es.statement.body[0].body[2].body[6].body[2].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[7].text == ':'
    assert es.statement.body[0].body[2].body[7].type == TokenType.Colon
    assert es.statement.body[0].body[2].body[8].body[0].text == '4'
    assert es.statement.body[0].body[2].body[8].body[0].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[8].body[1].text == '+'
    assert es.statement.body[0].body[2].body[8].body[1].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[8].body[2].text == '1'
    assert es.statement.body[0].body[2].body[8].body[2].type == TokenType.RealNumber
    assert es.statement.body[0].body[2].body[8].body[3].text == '+'
    assert es.statement.body[0].body[2].body[8].body[3].type == TokenType.Plus
    assert es.statement.body[0].body[2].body[8].body[4].text == '2'
    assert es.statement.body[0].body[2].body[8].body[4].type == TokenType.RealNumber

    assert es.statement.body[0].body[3].text == ','
    assert es.statement.body[0].body[3].type == TokenType.Comma
    assert es.statement.body[0].body[4].text == '111'
    assert es.statement.body[0].body[4].type == TokenType.RealNumber
    assert es.statement.body[0].body[5].text == ')'
    assert es.statement.body[0].body[5].type == TokenType.Rp
    assert es.statement.text == s.getvalue()


def case6():
    s = StringIO("taDate(a+b==1?(2+3):4+1+2,111)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'taDate'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0).text == 'a'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 1).text == '+'
    assert es.statement.matrix(0, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 2).text == 'b'
    assert es.statement.matrix(0, 2, 2).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 3).text == '=='
    assert es.statement.matrix(0, 2, 3).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 4).text == '1'
    assert es.statement.matrix(0, 2, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 5).text == '?'
    assert es.statement.matrix(0, 2, 5).type == TokenType.Question
    assert es.statement.matrix(0, 2, 6, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 6, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 6, 0, 1, 0).text == '2'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 6, 0, 1, 1).text == '+'
    assert es.statement.matrix(0, 2, 6, 0, 1, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 6, 0, 1, 2).text == '3'
    assert es.statement.matrix(0, 2, 6, 0, 1, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 6, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 6, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 7).text == ':'
    assert es.statement.matrix(0, 2, 7).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 8, 0).text == '4'
    assert es.statement.matrix(0, 2, 8, 0).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 8, 1).text == '+'
    assert es.statement.matrix(0, 2, 8, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 8, 2).text == '1'
    assert es.statement.matrix(0, 2, 8, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 8, 3).text == '+'
    assert es.statement.matrix(0, 2, 8, 3).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 8, 4).text == '2'
    assert es.statement.matrix(0, 2, 8, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4).text == '111'
    assert es.statement.matrix(0, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp

    assert es.statement.text == s.getvalue()


def case7():
    s = StringIO("taDate(a+b==1?(data(2+3)?(x+1):ddd):4+1+2,111)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'taDate'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0).text == 'a'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 1).text == '+'
    assert es.statement.matrix(0, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 2).text == 'b'
    assert es.statement.matrix(0, 2, 2).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 3).text == '=='
    assert es.statement.matrix(0, 2, 3).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 4).text == '1'
    assert es.statement.matrix(0, 2, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 5).text == '?'
    assert es.statement.matrix(0, 2, 5).type == TokenType.Question
    assert es.statement.matrix(0, 2, 6, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 6, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 0).text == 'data'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 2, 0).text == '2'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 2, 0).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 2, 1).text == '+'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 2, 2).text == '3'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 2, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 6, 0, 1, 1).text == '?'
    assert es.statement.matrix(0, 2, 6, 0, 1, 1).type == TokenType.Question
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 1, 0).text == 'x'
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 1, 1).text == '+'
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 1, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 1, 2).text == '1'
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 1, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 6, 0, 1, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 6, 0, 1, 3).text == ':'
    assert es.statement.matrix(0, 2, 6, 0, 1, 3).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 6, 0, 1, 4).text == 'ddd'
    assert es.statement.matrix(0, 2, 6, 0, 1, 4).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 6, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 6, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 7).text == ':'
    assert es.statement.matrix(0, 2, 7).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 8, 0).text == '4'
    assert es.statement.matrix(0, 2, 8, 0).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 8, 1).text == '+'
    assert es.statement.matrix(0, 2, 8, 1).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 8, 2).text == '1'
    assert es.statement.matrix(0, 2, 8, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 8, 3).text == '+'
    assert es.statement.matrix(0, 2, 8, 3).type == TokenType.Plus
    assert es.statement.matrix(0, 2, 8, 4).text == '2'
    assert es.statement.matrix(0, 2, 8, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4).text == '111'
    assert es.statement.matrix(0, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp

    assert es.statement.text == s.getvalue()


def case8():
    s = StringIO("a+b==1?(data(2+3)?(x+10):ddd):4+1+2+111")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'a'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(1).text == '+'
    assert es.statement.matrix(1).type == TokenType.Plus
    assert es.statement.matrix(2).text == 'b'
    assert es.statement.matrix(2).type == TokenType.Identifier
    assert es.statement.matrix(3).text == '=='
    assert es.statement.matrix(3).type == TokenType.Eq
    assert es.statement.matrix(4).text == '1'
    assert es.statement.matrix(4).type == TokenType.RealNumber
    assert es.statement.matrix(5).text == '?'
    assert es.statement.matrix(5).type == TokenType.Question
    assert es.statement.matrix(6, 0, 0).text == '('
    assert es.statement.matrix(6, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(6, 0, 1, 0, 0).text == 'data'
    assert es.statement.matrix(6, 0, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 1, 0, 1).text == '('
    assert es.statement.matrix(6, 0, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(6, 0, 1, 0, 2, 0).text == '2'
    assert es.statement.matrix(6, 0, 1, 0, 2, 0).type == TokenType.RealNumber
    assert es.statement.matrix(6, 0, 1, 0, 2, 1).text == '+'
    assert es.statement.matrix(6, 0, 1, 0, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(6, 0, 1, 0, 2, 2).text == '3'
    assert es.statement.matrix(6, 0, 1, 0, 2, 2).type == TokenType.RealNumber
    assert es.statement.matrix(6, 0, 1, 0, 3).text == ')'
    assert es.statement.matrix(6, 0, 1, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(6, 0, 1, 1).text == '?'
    assert es.statement.matrix(6, 0, 1, 1).type == TokenType.Question
    assert es.statement.matrix(6, 0, 1, 2, 0, 0).text == '('
    assert es.statement.matrix(6, 0, 1, 2, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(6, 0, 1, 2, 0, 1, 0).text == 'x'
    assert es.statement.matrix(6, 0, 1, 2, 0, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 1, 2, 0, 1, 1).text == '+'
    assert es.statement.matrix(6, 0, 1, 2, 0, 1, 1).type == TokenType.Plus
    assert es.statement.matrix(6, 0, 1, 2, 0, 1, 2).text == '10'
    assert es.statement.matrix(6, 0, 1, 2, 0, 1, 2).type == TokenType.RealNumber
    assert es.statement.matrix(6, 0, 1, 2, 0, 2).text == ')'
    assert es.statement.matrix(6, 0, 1, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(6, 0, 1, 3).text == ':'
    assert es.statement.matrix(6, 0, 1, 3).type == TokenType.Colon
    assert es.statement.matrix(6, 0, 1, 4).text == 'ddd'
    assert es.statement.matrix(6, 0, 1, 4).type == TokenType.Identifier

    assert es.statement.matrix(6, 0, 2).text == ')'
    assert es.statement.matrix(6, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(7).text == ':'
    assert es.statement.matrix(7).type == TokenType.Colon
    assert es.statement.matrix(8, 0).text == '4'
    assert es.statement.matrix(8, 0).type == TokenType.RealNumber
    assert es.statement.matrix(8, 1).text == '+'
    assert es.statement.matrix(8, 1).type == TokenType.Plus
    assert es.statement.matrix(8, 2).text == '1'
    assert es.statement.matrix(8, 2).type == TokenType.RealNumber
    assert es.statement.matrix(8, 3).text == '+'
    assert es.statement.matrix(8, 3).type == TokenType.Plus
    assert es.statement.matrix(8, 4).text == '2'
    assert es.statement.matrix(8, 4).type == TokenType.RealNumber
    assert es.statement.matrix(8, 5).text == '+'
    assert es.statement.matrix(8, 5).type == TokenType.Plus
    assert es.statement.matrix(8, 6).text == '111'
    assert es.statement.matrix(8, 6).type == TokenType.RealNumber

    assert es.statement.text == s.getvalue()


def case9():
    s = StringIO(
        "autoValue((toNum($*.*.EGORRES.881)!=''&&toNum($*.*.EGORRES.879)!=''?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), \"1\"):\"\"), true)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'autoValue'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 0, 2).text == '$*.*.EGORRES.881'
    assert es.statement.matrix(0, 2, 0, 1, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 1).text == '!='
    assert es.statement.matrix(0, 2, 0, 1, 1).type == TokenType.NEq
    assert es.statement.matrix(0, 2, 0, 1, 2).text == "''"
    assert es.statement.matrix(0, 2, 0, 1, 2).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 3).text == '&&'
    assert es.statement.matrix(0, 2, 0, 1, 3).type == TokenType.And
    assert es.statement.matrix(0, 2, 0, 1, 4, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 4, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 4, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 4, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 4, 2).text == '$*.*.EGORRES.879'
    assert es.statement.matrix(0, 2, 0, 1, 4, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 4, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 4, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 5).text == '!='
    assert es.statement.matrix(0, 2, 0, 1, 5).type == TokenType.NEq
    assert es.statement.matrix(0, 2, 0, 1, 6).text == "''"
    assert es.statement.matrix(0, 2, 0, 1, 6).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 7).text == '?'
    assert es.statement.matrix(0, 2, 0, 1, 7).type == TokenType.Question
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 0).text == 'RoundN'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 2).text == '$*.*.EGORRES.879'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 1).text == '/'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 1).type == TokenType.Divide
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 0).text == 'Math.pow'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 2).text == '$*.*.EGORRES.881'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 1).text == '/'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 1).type == TokenType.Divide
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 2).text == '1000'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 2).type == TokenType.Rp

    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 1).text == '0.33'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 1).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 1).text == '"1"'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 1).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 5).type == TokenType.Rp

    assert es.statement.matrix(0, 2, 0, 1, 9).text == ':'
    assert es.statement.matrix(0, 2, 0, 1, 9).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 0, 1, 10).text == '""'
    assert es.statement.matrix(0, 2, 0, 1, 10).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4, 0).text == ' '
    assert es.statement.matrix(0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 4, 1).text == 'true'
    assert es.statement.matrix(0, 4, 1).type == TokenType.TRUE
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp

    assert es.statement.text == s.getvalue()


def case10():
    s = StringIO("$*.*.*=='Y'&&mustAnswer($*.Demographics.AGE)?toNum($*.Demographics.AGE)>=18:true")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == '$*.*.*'
    assert es.statement.matrix(0, 0).type == TokenType.Variable
    assert es.statement.matrix(1).text == '=='
    assert es.statement.matrix(1).type == TokenType.Eq
    assert es.statement.matrix(2).text == "'Y'"
    assert es.statement.matrix(2).type == TokenType.Identifier
    assert es.statement.matrix(3).text == '&&'
    assert es.statement.matrix(3).type == TokenType.And
    assert es.statement.matrix(4, 0).text == 'mustAnswer'
    assert es.statement.matrix(4, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 1).text == '('
    assert es.statement.matrix(4, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 2).text == '$*.Demographics.AGE'
    assert es.statement.matrix(4, 2).type == TokenType.Variable
    assert es.statement.matrix(4, 3).text == ')'
    assert es.statement.matrix(4, 3).type == TokenType.Rp
    assert es.statement.matrix(5).text == '?'
    assert es.statement.matrix(5).type == TokenType.Question
    assert es.statement.matrix(6, 0, 0).text == 'toNum'
    assert es.statement.matrix(6, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 1).text == '('
    assert es.statement.matrix(6, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(6, 0, 2).text == '$*.Demographics.AGE'
    assert es.statement.matrix(6, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(6, 0, 3).text == ')'
    assert es.statement.matrix(6, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(6, 1).text == '>='
    assert es.statement.matrix(6, 1).type == TokenType.Ge
    assert es.statement.matrix(6, 2).text == '18'
    assert es.statement.matrix(6, 2).type == TokenType.RealNumber
    assert es.statement.matrix(7).text == ':'
    assert es.statement.matrix(7).type == TokenType.Colon
    assert es.statement.matrix(8).text == 'true'
    assert es.statement.matrix(8).type == TokenType.TRUE
    assert es.statement.text == s.getvalue()


def case11():
    s = StringIO("taDate(a == 1?(x == 1?y:z): false, a)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'taDate'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0).text == 'a'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 1).text == ' '
    assert es.statement.matrix(0, 2, 1).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 2).text == '=='
    assert es.statement.matrix(0, 2, 2).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 3).text == ' '
    assert es.statement.matrix(0, 2, 3).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 4).text == '1'
    assert es.statement.matrix(0, 2, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 5).text == '?'
    assert es.statement.matrix(0, 2, 5).type == TokenType.Question
    assert es.statement.matrix(0, 2, 6, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 6, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 6, 0, 1, 0).text == 'x'
    assert es.statement.matrix(0, 2, 6, 0, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 6, 0, 1, 1).text == ' '
    assert es.statement.matrix(0, 2, 6, 0, 1, 1).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 6, 0, 1, 2).text == '=='
    assert es.statement.matrix(0, 2, 6, 0, 1, 2).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 6, 0, 1, 3).text == ' '
    assert es.statement.matrix(0, 2, 6, 0, 1, 3).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 6, 0, 1, 4).text == '1'
    assert es.statement.matrix(0, 2, 6, 0, 1, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 6, 0, 1, 5).text == '?'
    assert es.statement.matrix(0, 2, 6, 0, 1, 5).type == TokenType.Question
    assert es.statement.matrix(0, 2, 6, 0, 1, 6).text == 'y'
    assert es.statement.matrix(0, 2, 6, 0, 1, 6).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 6, 0, 1, 7).text == ':'
    assert es.statement.matrix(0, 2, 6, 0, 1, 7).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 6, 0, 1, 8).text == 'z'
    assert es.statement.matrix(0, 2, 6, 0, 1, 8).type == TokenType.Identifier

    assert es.statement.matrix(0, 2, 6, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 6, 0, 2).type == TokenType.Rp

    assert es.statement.matrix(0, 2, 7).text == ':'
    assert es.statement.matrix(0, 2, 7).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 8, 0).text == ' '
    assert es.statement.matrix(0, 2, 8, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 8, 1).text == 'false'
    assert es.statement.matrix(0, 2, 8, 1).type == TokenType.FALSE
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4, 0).text == ' '
    assert es.statement.matrix(0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 4, 1).text == 'a'
    assert es.statement.matrix(0, 4, 1).type == TokenType.Identifier
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp


def case12():
    s = StringIO(
        """toDate($*.*.*)!=""&&toDate(getMinByLog($*.Informed Consent.DSSTDAT))!=""?dateDiff(getMinByLog($*.Informed Consent.DSSTDAT),$*.*.*, "D")>0:true""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'toDate($*.*.*)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'toDate'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '$*.*.*'
    assert es.statement.matrix(0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '!='
    assert es.statement.matrix(1).type == TokenType.NEq
    assert es.statement.matrix(2).text == '""'
    assert es.statement.matrix(2).type == TokenType.Identifier
    assert es.statement.matrix(3).text == '&&'
    assert es.statement.matrix(3).type == TokenType.And
    assert es.statement.matrix(4).text == 'toDate(getMinByLog($*.Informed Consent.DSSTDAT))'
    assert es.statement.matrix(4).type == TokenType.Statement
    assert es.statement.matrix(4, 0).text == 'toDate'
    assert es.statement.matrix(4, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 1).text == '('
    assert es.statement.matrix(4, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 2).text == 'getMinByLog($*.Informed Consent.DSSTDAT)'
    assert es.statement.matrix(4, 2).type == TokenType.Statement
    assert es.statement.matrix(4, 2, 0).text == 'getMinByLog($*.Informed Consent.DSSTDAT)'
    assert es.statement.matrix(4, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 2, 0, 0).text == 'getMinByLog'
    assert es.statement.matrix(4, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 2, 0, 1).text == '('
    assert es.statement.matrix(4, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 2, 0, 2).text == '$*.Informed Consent.DSSTDAT'
    assert es.statement.matrix(4, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(4, 2, 0, 3).text == ')'
    assert es.statement.matrix(4, 2, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(4, 3).text == ')'
    assert es.statement.matrix(4, 3).type == TokenType.Rp
    assert es.statement.matrix(5).text == '!='
    assert es.statement.matrix(5).type == TokenType.NEq
    assert es.statement.matrix(6).text == '""'
    assert es.statement.matrix(6).type == TokenType.Identifier
    assert es.statement.matrix(7).text == '?'
    assert es.statement.matrix(7).type == TokenType.Question
    assert es.statement.matrix(8).text == 'dateDiff(getMinByLog($*.Informed Consent.DSSTDAT),$*.*.*, "D")>0'
    assert es.statement.matrix(8).type == TokenType.Statement
    assert es.statement.matrix(8, 0).text == 'dateDiff(getMinByLog($*.Informed Consent.DSSTDAT),$*.*.*, "D")'
    assert es.statement.matrix(8, 0).type == TokenType.Statement
    assert es.statement.matrix(8, 0, 0).text == 'dateDiff'
    assert es.statement.matrix(8, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(8, 0, 1).text == '('
    assert es.statement.matrix(8, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(8, 0, 2).text == 'getMinByLog($*.Informed Consent.DSSTDAT)'
    assert es.statement.matrix(8, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(8, 0, 2, 0).text == 'getMinByLog($*.Informed Consent.DSSTDAT)'
    assert es.statement.matrix(8, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(8, 0, 2, 0, 0).text == 'getMinByLog'
    assert es.statement.matrix(8, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(8, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(8, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(8, 0, 2, 0, 2).text == '$*.Informed Consent.DSSTDAT'
    assert es.statement.matrix(8, 0, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(8, 0, 2, 0, 3).text == ')'
    assert es.statement.matrix(8, 0, 2, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(8, 0, 3).text == ','
    assert es.statement.matrix(8, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(8, 0, 4).text == '$*.*.*'
    assert es.statement.matrix(8, 0, 4).type == TokenType.Variable
    assert es.statement.matrix(8, 0, 5).text == ','
    assert es.statement.matrix(8, 0, 5).type == TokenType.Comma
    assert es.statement.matrix(8, 0, 6).text == ' "D"'
    assert es.statement.matrix(8, 0, 6).type == TokenType.Statement
    assert es.statement.matrix(8, 0, 6, 0).text == ' '
    assert es.statement.matrix(8, 0, 6, 0).type == TokenType.Blank
    assert es.statement.matrix(8, 0, 6, 1).text == '"D"'
    assert es.statement.matrix(8, 0, 6, 1).type == TokenType.Identifier
    assert es.statement.matrix(8, 0, 7).text == ')'
    assert es.statement.matrix(8, 0, 7).type == TokenType.Rp
    assert es.statement.matrix(8, 1).text == '>'
    assert es.statement.matrix(8, 1).type == TokenType.Gt
    assert es.statement.matrix(8, 2).text == '0'
    assert es.statement.matrix(8, 2).type == TokenType.RealNumber
    assert es.statement.matrix(9).text == ':'
    assert es.statement.matrix(9).type == TokenType.Colon
    assert es.statement.matrix(10).text == 'true'
    assert es.statement.matrix(10).type == TokenType.TRUE
    # es.statement.display([])


def case13():
    s = StringIO("""isValidDate($*.*.*)""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'isValidDate($*.*.*)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'isValidDate'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '$*.*.*'
    assert es.statement.matrix(0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp


def case14():
    s = StringIO(
        """autoValue((toNum($*.*.EGORRES.881)!=''&&toNum($*.*.EGORRES.879)!=''?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), "1"):""), true)""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(
        0).text == """autoValue((toNum($*.*.EGORRES.881)!=''&&toNum($*.*.EGORRES.879)!=''?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), \"1\"):\"\"), true)"""
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'autoValue'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0,
                               2).text == """(toNum($*.*.EGORRES.881)!=\'\'&&toNum($*.*.EGORRES.879)!=\'\'?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), \"1\"):\"\")"""
    assert es.statement.matrix(0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2,
                               0).text == """(toNum($*.*.EGORRES.881)!=\'\'&&toNum($*.*.EGORRES.879)!=\'\'?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), \"1\"):\"\")"""
    assert es.statement.matrix(0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0,
                               1).text == """toNum($*.*.EGORRES.881)!=\'\'&&toNum($*.*.EGORRES.879)!=\'\'?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), \"1\"):\"\""""
    assert es.statement.matrix(0, 2, 0, 1).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 0).text == 'toNum($*.*.EGORRES.881)'
    assert es.statement.matrix(0, 2, 0, 1, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 0, 2).text == '$*.*.EGORRES.881'
    assert es.statement.matrix(0, 2, 0, 1, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 1).text == '!='
    assert es.statement.matrix(0, 2, 0, 1, 1).type == TokenType.NEq
    assert es.statement.matrix(0, 2, 0, 1, 2).text == '\'\''
    assert es.statement.matrix(0, 2, 0, 1, 2).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 3).text == '&&'
    assert es.statement.matrix(0, 2, 0, 1, 3).type == TokenType.And
    assert es.statement.matrix(0, 2, 0, 1, 4).text == 'toNum($*.*.EGORRES.879)'
    assert es.statement.matrix(0, 2, 0, 1, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 4, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 4, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 4, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 4, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 4, 2).text == '$*.*.EGORRES.879'
    assert es.statement.matrix(0, 2, 0, 1, 4, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 4, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 4, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 5).text == '!='
    assert es.statement.matrix(0, 2, 0, 1, 5).type == TokenType.NEq
    assert es.statement.matrix(0, 2, 0, 1, 6).text == '\'\''
    assert es.statement.matrix(0, 2, 0, 1, 6).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 7).text == '?'
    assert es.statement.matrix(0, 2, 0, 1, 7).type == TokenType.Question
    assert es.statement.matrix(0, 2, 0, 1,
                               8).text == 'RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), "1")'
    assert es.statement.matrix(0, 2, 0, 1, 8).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8,
                               0).text == 'RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), "1")'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 0).text == 'RoundN'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0,
                               2).text == 'toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33)'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0).text == 'toNum($*.*.EGORRES.879)'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 2).text == '$*.*.EGORRES.879'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 1).text == '/'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 1).type == TokenType.Divide
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2).text == 'Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33)'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 0).text == 'Math.pow'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2).text == '(toNum($*.*.EGORRES.881)/1000)'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0).text == '(toNum($*.*.EGORRES.881)/1000)'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 0).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1).text == 'toNum($*.*.EGORRES.881)/1000'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0).text == 'toNum($*.*.EGORRES.881)'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 2).text == '$*.*.EGORRES.881'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 1).text == '/'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 1).type == TokenType.Divide
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 2).text == '1000'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 1, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4).text == ' 0.33'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 1).text == '0.33'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 4, 1).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 2, 2, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4).text == ' "1"'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 1).text == '"1"'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 4, 1).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 1, 8, 0, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 1, 9).text == ':'
    assert es.statement.matrix(0, 2, 0, 1, 9).type == TokenType.Colon
    assert es.statement.matrix(0, 2, 0, 1, 10).text == '""'
    assert es.statement.matrix(0, 2, 0, 1, 10).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4).text == ' true'
    assert es.statement.matrix(0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 4, 0).text == ' '
    assert es.statement.matrix(0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 4, 1).text == 'true'
    assert es.statement.matrix(0, 4, 1).type == TokenType.TRUE
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp


def case15():
    s = StringIO("$*.*.EGPERF==\"Y\"")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == '$*.*.EGPERF'
    assert es.statement.matrix(0).type == TokenType.Variable
    assert es.statement.matrix(1).text == '=='
    assert es.statement.matrix(1).type == TokenType.Eq
    assert es.statement.matrix(2).text == '"Y"'
    assert es.statement.matrix(2).type == TokenType.Identifier


def case16():
    s = StringIO("$*.*.EGORRES.12394==\"CS\"")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == '$*.*.EGORRES.12394'
    assert es.statement.matrix(0).type == TokenType.Variable
    assert es.statement.matrix(1).text == '=='
    assert es.statement.matrix(1).type == TokenType.Eq
    assert es.statement.matrix(2).text == '"CS"'
    assert es.statement.matrix(2).type == TokenType.Identifier


def case17():
    s = StringIO("""condition(mustAnswer(toNum($*.*.*)), isRange($*.*.*, 40,160))""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'condition(mustAnswer(toNum($*.*.*)), isRange($*.*.*, 40,160))'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'condition'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == 'mustAnswer(toNum($*.*.*))'
    assert es.statement.matrix(0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0).text == 'mustAnswer(toNum($*.*.*))'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 0).text == 'mustAnswer'
    assert es.statement.matrix(0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2).text == 'toNum($*.*.*)'
    assert es.statement.matrix(0, 2, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0).text == 'toNum($*.*.*)'
    assert es.statement.matrix(0, 2, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 0).text == 'toNum'
    assert es.statement.matrix(0, 2, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 2).text == '$*.*.*'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 3).text == ')'
    assert es.statement.matrix(0, 2, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4).text == ' isRange($*.*.*, 40,160)'
    assert es.statement.matrix(0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 4, 0).text == ' '
    assert es.statement.matrix(0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 4, 1).text == 'isRange($*.*.*, 40,160)'
    assert es.statement.matrix(0, 4, 1).type == TokenType.Statement
    assert es.statement.matrix(0, 4, 1, 0).text == 'isRange'
    assert es.statement.matrix(0, 4, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 4, 1, 1).text == '('
    assert es.statement.matrix(0, 4, 1, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 4, 1, 2).text == '$*.*.*'
    assert es.statement.matrix(0, 4, 1, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 4, 1, 3).text == ','
    assert es.statement.matrix(0, 4, 1, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4, 1, 4).text == ' 40'
    assert es.statement.matrix(0, 4, 1, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 4, 1, 4, 0).text == ' '
    assert es.statement.matrix(0, 4, 1, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 4, 1, 4, 1).text == '40'
    assert es.statement.matrix(0, 4, 1, 4, 1).type == TokenType.RealNumber
    assert es.statement.matrix(0, 4, 1, 5).text == ','
    assert es.statement.matrix(0, 4, 1, 5).type == TokenType.Comma
    assert es.statement.matrix(0, 4, 1, 6).text == '160'
    assert es.statement.matrix(0, 4, 1, 6).type == TokenType.RealNumber
    assert es.statement.matrix(0, 4, 1, 7).text == ')'
    assert es.statement.matrix(0, 4, 1, 7).type == TokenType.Rp
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp


def case18():
    s = StringIO("""mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='Y'?$*.*.*=='':true""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'mustAnswer($*.*.CRONGO)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'mustAnswer'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '$*.*.CRONGO'
    assert es.statement.matrix(0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '&&'
    assert es.statement.matrix(1).type == TokenType.And
    assert es.statement.matrix(2).text == '$*.*.CRONGO'
    assert es.statement.matrix(2).type == TokenType.Variable
    assert es.statement.matrix(3).text == '=='
    assert es.statement.matrix(3).type == TokenType.Eq
    assert es.statement.matrix(4).text == '\'Y\''
    assert es.statement.matrix(4).type == TokenType.Identifier
    assert es.statement.matrix(5).text == '?'
    assert es.statement.matrix(5).type == TokenType.Question
    assert es.statement.matrix(6).text == '$*.*.*==\'\''
    assert es.statement.matrix(6).type == TokenType.Statement
    assert es.statement.matrix(6, 0).text == '$*.*.*'
    assert es.statement.matrix(6, 0).type == TokenType.Variable
    assert es.statement.matrix(6, 1).text == '=='
    assert es.statement.matrix(6, 1).type == TokenType.Eq
    assert es.statement.matrix(6, 2).text == '\'\''
    assert es.statement.matrix(6, 2).type == TokenType.Identifier
    assert es.statement.matrix(7).text == ':'
    assert es.statement.matrix(7).type == TokenType.Colon
    assert es.statement.matrix(8).text == 'true'
    assert es.statement.matrix(8).type == TokenType.TRUE


def case19():
    s = StringIO("""mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'?$*.*.*!='':true""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'mustAnswer($*.*.CRONGO)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'mustAnswer'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '$*.*.CRONGO'
    assert es.statement.matrix(0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '&&'
    assert es.statement.matrix(1).type == TokenType.And
    assert es.statement.matrix(2).text == '$*.*.CRONGO'
    assert es.statement.matrix(2).type == TokenType.Variable
    assert es.statement.matrix(3).text == '=='
    assert es.statement.matrix(3).type == TokenType.Eq
    assert es.statement.matrix(4).text == '\'N\''
    assert es.statement.matrix(4).type == TokenType.Identifier
    assert es.statement.matrix(5).text == '?'
    assert es.statement.matrix(5).type == TokenType.Question
    assert es.statement.matrix(6).text == '$*.*.*!=\'\''
    assert es.statement.matrix(6).type == TokenType.Statement
    assert es.statement.matrix(6, 0).text == '$*.*.*'
    assert es.statement.matrix(6, 0).type == TokenType.Variable
    assert es.statement.matrix(6, 1).text == '!='
    assert es.statement.matrix(6, 1).type == TokenType.NEq
    assert es.statement.matrix(6, 2).text == '\'\''
    assert es.statement.matrix(6, 2).type == TokenType.Identifier
    assert es.statement.matrix(7).text == ':'
    assert es.statement.matrix(7).type == TokenType.Colon
    assert es.statement.matrix(8).text == 'true'
    assert es.statement.matrix(8).type == TokenType.TRUE


def case20():
    s = StringIO("""autoIncrease(1,1,1,1)""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'autoIncrease(1,1,1,1)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'autoIncrease'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '1'
    assert es.statement.matrix(0, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4).text == '1'
    assert es.statement.matrix(0, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 5).text == ','
    assert es.statement.matrix(0, 5).type == TokenType.Comma
    assert es.statement.matrix(0, 6).text == '1'
    assert es.statement.matrix(0, 6).type == TokenType.RealNumber
    assert es.statement.matrix(0, 7).text == ','
    assert es.statement.matrix(0, 7).type == TokenType.Comma
    assert es.statement.matrix(0, 8).text == '1'
    assert es.statement.matrix(0, 8).type == TokenType.RealNumber
    assert es.statement.matrix(0, 9).text == ')'
    assert es.statement.matrix(0, 9).type == TokenType.Rp


def case21():
    s = StringIO("""$*.*.*=='Y'&&mustAnswer($*.Demographics.AGE)?toNum($*.Demographics.AGE)>=18:true""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == '$*.*.*'
    assert es.statement.matrix(0).type == TokenType.Variable
    assert es.statement.matrix(1).text == '=='
    assert es.statement.matrix(1).type == TokenType.Eq
    assert es.statement.matrix(2).text == '\'Y\''
    assert es.statement.matrix(2).type == TokenType.Identifier
    assert es.statement.matrix(3).text == '&&'
    assert es.statement.matrix(3).type == TokenType.And
    assert es.statement.matrix(4).text == 'mustAnswer($*.Demographics.AGE)'
    assert es.statement.matrix(4).type == TokenType.Statement
    assert es.statement.matrix(4, 0).text == 'mustAnswer'
    assert es.statement.matrix(4, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 1).text == '('
    assert es.statement.matrix(4, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 2).text == '$*.Demographics.AGE'
    assert es.statement.matrix(4, 2).type == TokenType.Variable
    assert es.statement.matrix(4, 3).text == ')'
    assert es.statement.matrix(4, 3).type == TokenType.Rp
    assert es.statement.matrix(5).text == '?'
    assert es.statement.matrix(5).type == TokenType.Question
    assert es.statement.matrix(6).text == 'toNum($*.Demographics.AGE)>=18'
    assert es.statement.matrix(6).type == TokenType.Statement
    assert es.statement.matrix(6, 0).text == 'toNum($*.Demographics.AGE)'
    assert es.statement.matrix(6, 0).type == TokenType.Statement
    assert es.statement.matrix(6, 0, 0).text == 'toNum'
    assert es.statement.matrix(6, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 1).text == '('
    assert es.statement.matrix(6, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(6, 0, 2).text == '$*.Demographics.AGE'
    assert es.statement.matrix(6, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(6, 0, 3).text == ')'
    assert es.statement.matrix(6, 0, 3).type == TokenType.Rp
    assert es.statement.matrix(6, 1).text == '>='
    assert es.statement.matrix(6, 1).type == TokenType.Ge
    assert es.statement.matrix(6, 2).text == '18'
    assert es.statement.matrix(6, 2).type == TokenType.RealNumber
    assert es.statement.matrix(7).text == ':'
    assert es.statement.matrix(7).type == TokenType.Colon
    assert es.statement.matrix(8).text == 'true'
    assert es.statement.matrix(8).type == TokenType.TRUE


def case22():
    s = StringIO(
        """mustAnswer($*.*.*)&&(getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)=='V1.5'||getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)=='V1.6')?($*.*.*=='0'||$*.*.*=='1'||$*.*.*=='2'):true""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'mustAnswer($*.*.*)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'mustAnswer'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '$*.*.*'
    assert es.statement.matrix(0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '&&'
    assert es.statement.matrix(1).type == TokenType.And
    assert es.statement.matrix(
        2).text == '(getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)==\'V1.5\'||getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)==\'V1.6\')'
    assert es.statement.matrix(2).type == TokenType.Statement
    assert es.statement.matrix(2, 0).text == '('
    assert es.statement.matrix(2, 0).type == TokenType.Lp
    assert es.statement.matrix(2,
                               1).text == 'getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)==\'V1.5\'||getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)==\'V1.6\''
    assert es.statement.matrix(2, 1).type == TokenType.Statement
    assert es.statement.matrix(2, 1,
                               0).text == 'getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)'
    assert es.statement.matrix(2, 1, 0).type == TokenType.Statement
    assert es.statement.matrix(2, 1, 0, 0).text == 'getICFVersion'
    assert es.statement.matrix(2, 1, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(2, 1, 0, 1).text == '('
    assert es.statement.matrix(2, 1, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(2, 1, 0, 2).text == '$*.Date of Visit.SVDAT'
    assert es.statement.matrix(2, 1, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(2, 1, 0, 3).text == ','
    assert es.statement.matrix(2, 1, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(2, 1, 0, 4).text == ' $*.Informed Consent.DSSTDAT'
    assert es.statement.matrix(2, 1, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(2, 1, 0, 4, 0).text == ' '
    assert es.statement.matrix(2, 1, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(2, 1, 0, 4, 1).text == '$*.Informed Consent.DSSTDAT'
    assert es.statement.matrix(2, 1, 0, 4, 1).type == TokenType.Variable
    assert es.statement.matrix(2, 1, 0, 5).text == ','
    assert es.statement.matrix(2, 1, 0, 5).type == TokenType.Comma
    assert es.statement.matrix(2, 1, 0, 6).text == ' $*.Informed Consent.VERSION'
    assert es.statement.matrix(2, 1, 0, 6).type == TokenType.Statement
    assert es.statement.matrix(2, 1, 0, 6, 0).text == ' '
    assert es.statement.matrix(2, 1, 0, 6, 0).type == TokenType.Blank
    assert es.statement.matrix(2, 1, 0, 6, 1).text == '$*.Informed Consent.VERSION'
    assert es.statement.matrix(2, 1, 0, 6, 1).type == TokenType.Variable
    assert es.statement.matrix(2, 1, 0, 7).text == ')'
    assert es.statement.matrix(2, 1, 0, 7).type == TokenType.Rp
    assert es.statement.matrix(2, 1, 1).text == '=='
    assert es.statement.matrix(2, 1, 1).type == TokenType.Eq
    assert es.statement.matrix(2, 1, 2).text == '\'V1.5\''
    assert es.statement.matrix(2, 1, 2).type == TokenType.Identifier
    assert es.statement.matrix(2, 1, 3).text == '||'
    assert es.statement.matrix(2, 1, 3).type == TokenType.Or
    assert es.statement.matrix(2, 1,
                               4).text == 'getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)'
    assert es.statement.matrix(2, 1, 4).type == TokenType.Statement
    assert es.statement.matrix(2, 1, 4, 0).text == 'getICFVersion'
    assert es.statement.matrix(2, 1, 4, 0).type == TokenType.Identifier
    assert es.statement.matrix(2, 1, 4, 1).text == '('
    assert es.statement.matrix(2, 1, 4, 1).type == TokenType.Lp
    assert es.statement.matrix(2, 1, 4, 2).text == '$*.Date of Visit.SVDAT'
    assert es.statement.matrix(2, 1, 4, 2).type == TokenType.Variable
    assert es.statement.matrix(2, 1, 4, 3).text == ','
    assert es.statement.matrix(2, 1, 4, 3).type == TokenType.Comma
    assert es.statement.matrix(2, 1, 4, 4).text == ' $*.Informed Consent.DSSTDAT'
    assert es.statement.matrix(2, 1, 4, 4).type == TokenType.Statement
    assert es.statement.matrix(2, 1, 4, 4, 0).text == ' '
    assert es.statement.matrix(2, 1, 4, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(2, 1, 4, 4, 1).text == '$*.Informed Consent.DSSTDAT'
    assert es.statement.matrix(2, 1, 4, 4, 1).type == TokenType.Variable
    assert es.statement.matrix(2, 1, 4, 5).text == ','
    assert es.statement.matrix(2, 1, 4, 5).type == TokenType.Comma
    assert es.statement.matrix(2, 1, 4, 6).text == ' $*.Informed Consent.VERSION'
    assert es.statement.matrix(2, 1, 4, 6).type == TokenType.Statement
    assert es.statement.matrix(2, 1, 4, 6, 0).text == ' '
    assert es.statement.matrix(2, 1, 4, 6, 0).type == TokenType.Blank
    assert es.statement.matrix(2, 1, 4, 6, 1).text == '$*.Informed Consent.VERSION'
    assert es.statement.matrix(2, 1, 4, 6, 1).type == TokenType.Variable
    assert es.statement.matrix(2, 1, 4, 7).text == ')'
    assert es.statement.matrix(2, 1, 4, 7).type == TokenType.Rp
    assert es.statement.matrix(2, 1, 5).text == '=='
    assert es.statement.matrix(2, 1, 5).type == TokenType.Eq
    assert es.statement.matrix(2, 1, 6).text == '\'V1.6\''
    assert es.statement.matrix(2, 1, 6).type == TokenType.Identifier
    assert es.statement.matrix(2, 2).text == ')'
    assert es.statement.matrix(2, 2).type == TokenType.Rp
    assert es.statement.matrix(3).text == '?'
    assert es.statement.matrix(3).type == TokenType.Question
    assert es.statement.matrix(4).text == '($*.*.*==\'0\'||$*.*.*==\'1\'||$*.*.*==\'2\')'
    assert es.statement.matrix(4).type == TokenType.Statement
    assert es.statement.matrix(4, 0).text == '($*.*.*==\'0\'||$*.*.*==\'1\'||$*.*.*==\'2\')'
    assert es.statement.matrix(4, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 0).text == '('
    assert es.statement.matrix(4, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(4, 0, 1).text == '$*.*.*==\'0\'||$*.*.*==\'1\'||$*.*.*==\'2\''
    assert es.statement.matrix(4, 0, 1).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 1, 0).text == '$*.*.*'
    assert es.statement.matrix(4, 0, 1, 0).type == TokenType.Variable
    assert es.statement.matrix(4, 0, 1, 1).text == '=='
    assert es.statement.matrix(4, 0, 1, 1).type == TokenType.Eq
    assert es.statement.matrix(4, 0, 1, 2).text == '\'0\''
    assert es.statement.matrix(4, 0, 1, 2).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 1, 3).text == '||'
    assert es.statement.matrix(4, 0, 1, 3).type == TokenType.Or
    assert es.statement.matrix(4, 0, 1, 4).text == '$*.*.*'
    assert es.statement.matrix(4, 0, 1, 4).type == TokenType.Variable
    assert es.statement.matrix(4, 0, 1, 5).text == '=='
    assert es.statement.matrix(4, 0, 1, 5).type == TokenType.Eq
    assert es.statement.matrix(4, 0, 1, 6).text == '\'1\''
    assert es.statement.matrix(4, 0, 1, 6).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 1, 7).text == '||'
    assert es.statement.matrix(4, 0, 1, 7).type == TokenType.Or
    assert es.statement.matrix(4, 0, 1, 8).text == '$*.*.*'
    assert es.statement.matrix(4, 0, 1, 8).type == TokenType.Variable
    assert es.statement.matrix(4, 0, 1, 9).text == '=='
    assert es.statement.matrix(4, 0, 1, 9).type == TokenType.Eq
    assert es.statement.matrix(4, 0, 1, 10).text == '\'2\''
    assert es.statement.matrix(4, 0, 1, 10).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 2).text == ')'
    assert es.statement.matrix(4, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(5).text == ':'
    assert es.statement.matrix(5).type == TokenType.Colon
    assert es.statement.matrix(6).text == 'true'
    assert es.statement.matrix(6).type == TokenType.TRUE


def case23():
    s = StringIO(
        """toDate($C1D1.ONC-392 Administration.ECSTDAT)!=""&& toDate($*.*.LBDAT)!=""&& toDate("2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00")!="" &&toDate("2015-1-12 "+$*.*.*+":00")!=""?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0:true""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'toDate($C1D1.ONC-392 Administration.ECSTDAT)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'toDate'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == '$C1D1.ONC-392 Administration.ECSTDAT'
    assert es.statement.matrix(0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '!='
    assert es.statement.matrix(1).type == TokenType.NEq
    assert es.statement.matrix(2).text == '""'
    assert es.statement.matrix(2).type == TokenType.Identifier
    assert es.statement.matrix(3).text == '&&'
    assert es.statement.matrix(3).type == TokenType.And
    assert es.statement.matrix(4).text == ' '
    assert es.statement.matrix(4).type == TokenType.Blank
    assert es.statement.matrix(5).text == 'toDate($*.*.LBDAT)'
    assert es.statement.matrix(5).type == TokenType.Statement
    assert es.statement.matrix(5, 0).text == 'toDate'
    assert es.statement.matrix(5, 0).type == TokenType.Identifier
    assert es.statement.matrix(5, 1).text == '('
    assert es.statement.matrix(5, 1).type == TokenType.Lp
    assert es.statement.matrix(5, 2).text == '$*.*.LBDAT'
    assert es.statement.matrix(5, 2).type == TokenType.Variable
    assert es.statement.matrix(5, 3).text == ')'
    assert es.statement.matrix(5, 3).type == TokenType.Rp
    assert es.statement.matrix(6).text == '!='
    assert es.statement.matrix(6).type == TokenType.NEq
    assert es.statement.matrix(7).text == '""'
    assert es.statement.matrix(7).type == TokenType.Identifier
    assert es.statement.matrix(8).text == '&&'
    assert es.statement.matrix(8).type == TokenType.And
    assert es.statement.matrix(9).text == ' '
    assert es.statement.matrix(9).type == TokenType.Blank
    assert es.statement.matrix(10).text == 'toDate("2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00")'
    assert es.statement.matrix(10).type == TokenType.Statement
    assert es.statement.matrix(10, 0).text == 'toDate'
    assert es.statement.matrix(10, 0).type == TokenType.Identifier
    assert es.statement.matrix(10, 1).text == '('
    assert es.statement.matrix(10, 1).type == TokenType.Lp
    assert es.statement.matrix(10, 2).text == '"2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00"'
    assert es.statement.matrix(10, 2).type == TokenType.Statement
    assert es.statement.matrix(10, 2, 0).text == '"2015-1-12 "'
    assert es.statement.matrix(10, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(10, 2, 1).text == '+'
    assert es.statement.matrix(10, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(10, 2, 2).text == '$C1D1.ONC-392 Administration.ECSTTIM'
    assert es.statement.matrix(10, 2, 2).type == TokenType.Variable
    assert es.statement.matrix(10, 2, 3).text == '+'
    assert es.statement.matrix(10, 2, 3).type == TokenType.Plus
    assert es.statement.matrix(10, 2, 4).text == '":00"'
    assert es.statement.matrix(10, 2, 4).type == TokenType.Identifier
    assert es.statement.matrix(10, 3).text == ')'
    assert es.statement.matrix(10, 3).type == TokenType.Rp
    assert es.statement.matrix(11).text == '!='
    assert es.statement.matrix(11).type == TokenType.NEq
    assert es.statement.matrix(12).text == '""'
    assert es.statement.matrix(12).type == TokenType.Identifier
    assert es.statement.matrix(13).text == ' '
    assert es.statement.matrix(13).type == TokenType.Blank
    assert es.statement.matrix(14).text == '&&'
    assert es.statement.matrix(14).type == TokenType.And
    assert es.statement.matrix(15).text == 'toDate("2015-1-12 "+$*.*.*+":00")'
    assert es.statement.matrix(15).type == TokenType.Statement
    assert es.statement.matrix(15, 0).text == 'toDate'
    assert es.statement.matrix(15, 0).type == TokenType.Identifier
    assert es.statement.matrix(15, 1).text == '('
    assert es.statement.matrix(15, 1).type == TokenType.Lp
    assert es.statement.matrix(15, 2).text == '"2015-1-12 "+$*.*.*+":00"'
    assert es.statement.matrix(15, 2).type == TokenType.Statement
    assert es.statement.matrix(15, 2, 0).text == '"2015-1-12 "'
    assert es.statement.matrix(15, 2, 0).type == TokenType.Identifier
    assert es.statement.matrix(15, 2, 1).text == '+'
    assert es.statement.matrix(15, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(15, 2, 2).text == '$*.*.*'
    assert es.statement.matrix(15, 2, 2).type == TokenType.Variable
    assert es.statement.matrix(15, 2, 3).text == '+'
    assert es.statement.matrix(15, 2, 3).type == TokenType.Plus
    assert es.statement.matrix(15, 2, 4).text == '":00"'
    assert es.statement.matrix(15, 2, 4).type == TokenType.Identifier
    assert es.statement.matrix(15, 3).text == ')'
    assert es.statement.matrix(15, 3).type == TokenType.Rp
    assert es.statement.matrix(16).text == '!='
    assert es.statement.matrix(16).type == TokenType.NEq
    assert es.statement.matrix(17).text == '""'
    assert es.statement.matrix(17).type == TokenType.Identifier
    assert es.statement.matrix(18).text == '?'
    assert es.statement.matrix(18).type == TokenType.Question
    assert es.statement.matrix(
        19).text == 'dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0'
    assert es.statement.matrix(19).type == TokenType.Statement
    assert es.statement.matrix(19,
                               0).text == 'dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")'
    assert es.statement.matrix(19, 0).type == TokenType.Statement
    assert es.statement.matrix(19, 0, 0).text == 'dateDiff'
    assert es.statement.matrix(19, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(19, 0, 1).text == '('
    assert es.statement.matrix(19, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(19, 0,
                               2).text == '$C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00"'
    assert es.statement.matrix(19, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(19, 0, 2, 0).text == '$C1D1.ONC-392 Administration.ECSTDAT'
    assert es.statement.matrix(19, 0, 2, 0).type == TokenType.Variable
    assert es.statement.matrix(19, 0, 2, 1).text == '+'
    assert es.statement.matrix(19, 0, 2, 1).type == TokenType.Plus
    assert es.statement.matrix(19, 0, 2, 2).text == '" "'
    assert es.statement.matrix(19, 0, 2, 2).type == TokenType.Identifier
    assert es.statement.matrix(19, 0, 2, 3).text == '+'
    assert es.statement.matrix(19, 0, 2, 3).type == TokenType.Plus
    assert es.statement.matrix(19, 0, 2, 4).text == '$C1D1.ONC-392 Administration.ECSTTIM'
    assert es.statement.matrix(19, 0, 2, 4).type == TokenType.Variable
    assert es.statement.matrix(19, 0, 2, 5).text == '+'
    assert es.statement.matrix(19, 0, 2, 5).type == TokenType.Plus
    assert es.statement.matrix(19, 0, 2, 6).text == '":00"'
    assert es.statement.matrix(19, 0, 2, 6).type == TokenType.Identifier
    assert es.statement.matrix(19, 0, 3).text == ','
    assert es.statement.matrix(19, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(19, 0, 4).text == '$*.*.LBDAT+" "+$*.*.*+":00"'
    assert es.statement.matrix(19, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(19, 0, 4, 0).text == '$*.*.LBDAT'
    assert es.statement.matrix(19, 0, 4, 0).type == TokenType.Variable
    assert es.statement.matrix(19, 0, 4, 1).text == '+'
    assert es.statement.matrix(19, 0, 4, 1).type == TokenType.Plus
    assert es.statement.matrix(19, 0, 4, 2).text == '" "'
    assert es.statement.matrix(19, 0, 4, 2).type == TokenType.Identifier
    assert es.statement.matrix(19, 0, 4, 3).text == '+'
    assert es.statement.matrix(19, 0, 4, 3).type == TokenType.Plus
    assert es.statement.matrix(19, 0, 4, 4).text == '$*.*.*'
    assert es.statement.matrix(19, 0, 4, 4).type == TokenType.Variable
    assert es.statement.matrix(19, 0, 4, 5).text == '+'
    assert es.statement.matrix(19, 0, 4, 5).type == TokenType.Plus
    assert es.statement.matrix(19, 0, 4, 6).text == '":00"'
    assert es.statement.matrix(19, 0, 4, 6).type == TokenType.Identifier
    assert es.statement.matrix(19, 0, 5).text == ','
    assert es.statement.matrix(19, 0, 5).type == TokenType.Comma
    assert es.statement.matrix(19, 0, 6).text == '"m"'
    assert es.statement.matrix(19, 0, 6).type == TokenType.Identifier
    assert es.statement.matrix(19, 0, 7).text == ')'
    assert es.statement.matrix(19, 0, 7).type == TokenType.Rp
    assert es.statement.matrix(19, 1).text == '>'
    assert es.statement.matrix(19, 1).type == TokenType.Gt
    assert es.statement.matrix(19, 2).text == '0'
    assert es.statement.matrix(19, 2).type == TokenType.RealNumber
    assert es.statement.matrix(20).text == ':'
    assert es.statement.matrix(20).type == TokenType.Colon
    assert es.statement.matrix(21).text == 'true'
    assert es.statement.matrix(21).type == TokenType.TRUE


def case24():
    s = StringIO(
        """autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01), true)""")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(
        0).text == 'autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01), true)'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'autoValue'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0,
                               2).text == 'RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01)'
    assert es.statement.matrix(0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2,
                               0).text == 'RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01)'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 0).text == 'RoundN'
    assert es.statement.matrix(0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0,
                               2).text == 'sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10))'
    assert es.statement.matrix(0, 2, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2,
                               0).text == 'sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10))'
    assert es.statement.matrix(0, 2, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 0).text == 'sum'
    assert es.statement.matrix(0, 2, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0,
                               2).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 2,
                               0).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM")'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 0).text == 'getSumOfItemInLog'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0,
                               2).text == '$*.Target Lesions Assessment (Details) (Screening).TLLONG'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0,
                               4).text == ' $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4,
                               1).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 1).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 2).text == '!='
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 2).type == TokenType.NEq
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 3).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 3).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 4).text == '11'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 5).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 5).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 6).text == '&&'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 6).type == TokenType.And
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 7).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 7).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4,
                               8).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 8).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 9).text == '=='
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 9).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 10).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 10).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 11).text == '"CM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 4, 11).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 0, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 1).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 2, 1).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0,
                               4).text == ' multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 4,
                               1).text == 'multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10)'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 0).text == 'multiply'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1,
                               2).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM")'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2,
                               0).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM")'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 0).text == 'getSumOfItemInLog'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0,
                               2).text == '$*.Target Lesions Assessment (Details) (Screening).TLLONG'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0,
                               4).text == ' $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4,
                               1).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 1).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 2).text == '!='
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 2).type == TokenType.NEq
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 3).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 3).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 4).text == '11'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 5).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 5).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 6).text == '&&'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 6).type == TokenType.And
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 7).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 7).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4,
                               8).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 8).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 9).text == '=='
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 9).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 10).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 10).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 11).text == '"MM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 4, 11).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 2, 0, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4).text == '1/10'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4, 0).text == '1'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4, 0).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4, 1).text == '/'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4, 1).type == TokenType.Divide
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4, 2).text == '10'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 4, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 1, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 2).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 4, 2).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 5).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 5).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0,
                               6).text == ' getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 6,
                               1).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM")'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 0).text == 'getSumOfItemInLog'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1,
                               2).text == '$*.Target Lesions Assessment (Details) (Screening).TLSHORT'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1,
                               4).text == ' $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4,
                               1).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 1).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 2).text == '=='
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 2).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 3).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 3).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 4).text == '11'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 5).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 5).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 6).text == '&&'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 6).type == TokenType.And
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 7).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 7).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4,
                               8).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 8).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 9).text == '=='
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 9).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 10).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 10).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 11).text == '"CM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 4, 11).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 1, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 2).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 6, 2).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 7).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 7).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0,
                               8).text == ' multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 8,
                               1).text == 'multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 0).text == 'multiply'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1,
                               2).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM")'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2,
                               0).text == 'getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM")'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 0).text == 'getSumOfItemInLog'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0,
                               2).text == '$*.Target Lesions Assessment (Details) (Screening).TLSHORT'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 2).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0,
                               4).text == ' $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4,
                               1).text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 1).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 2).text == '=='
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 2).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 3).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 3).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 4).text == '11'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 4).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 5).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 5).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 6).text == '&&'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 6).type == TokenType.And
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 7).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 7).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4,
                               8).text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 8).type == TokenType.Variable
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 9).text == '=='
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 9).type == TokenType.Eq
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 10).text == ' '
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 10).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 11).text == '"MM"'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 4, 11).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 2, 0, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4).text == '1/10'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4, 0).text == '1'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4, 0).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4, 1).text == '/'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4, 1).type == TokenType.Divide
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4, 2).text == '10'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 4, 2).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 8, 1, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 2, 0, 9).text == ')'
    assert es.statement.matrix(0, 2, 0, 2, 0, 9).type == TokenType.Rp
    assert es.statement.matrix(0, 2, 0, 3).text == ','
    assert es.statement.matrix(0, 2, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 2, 0, 4).text == ' 0.01'
    assert es.statement.matrix(0, 2, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 4, 0).text == ' '
    assert es.statement.matrix(0, 2, 0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 2, 0, 4, 1).text == '0.01'
    assert es.statement.matrix(0, 2, 0, 4, 1).type == TokenType.RealNumber
    assert es.statement.matrix(0, 2, 0, 5).text == ')'
    assert es.statement.matrix(0, 2, 0, 5).type == TokenType.Rp
    assert es.statement.matrix(0, 3).text == ','
    assert es.statement.matrix(0, 3).type == TokenType.Comma
    assert es.statement.matrix(0, 4).text == ' true'
    assert es.statement.matrix(0, 4).type == TokenType.Statement
    assert es.statement.matrix(0, 4, 0).text == ' '
    assert es.statement.matrix(0, 4, 0).type == TokenType.Blank
    assert es.statement.matrix(0, 4, 1).text == 'true'
    assert es.statement.matrix(0, 4, 1).type == TokenType.TRUE
    assert es.statement.matrix(0, 5).text == ')'
    assert es.statement.matrix(0, 5).type == TokenType.Rp


def case25():
    s = StringIO("a()")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0, 0).text == 'a'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == "("
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == ")"
    assert es.statement.matrix(0, 2).type == TokenType.Rp



def case26():
    s = StringIO("1==2?2+1:3==4?4:5")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == '1'
    assert es.statement.matrix(0).type == TokenType.RealNumber
    assert es.statement.matrix(1).text == '=='
    assert es.statement.matrix(1).type == TokenType.Eq
    assert es.statement.matrix(2).text == '2'
    assert es.statement.matrix(2).type == TokenType.RealNumber
    assert es.statement.matrix(3).text == '?'
    assert es.statement.matrix(3).type == TokenType.Question
    assert es.statement.matrix(4).text == '2+1'
    assert es.statement.matrix(4).type == TokenType.Statement
    assert es.statement.matrix(4, 0).text == '2'
    assert es.statement.matrix(4, 0).type == TokenType.RealNumber
    assert es.statement.matrix(4, 1).text == '+'
    assert es.statement.matrix(4, 1).type == TokenType.Plus
    assert es.statement.matrix(4, 2).text == '1'
    assert es.statement.matrix(4, 2).type == TokenType.RealNumber
    assert es.statement.matrix(5).text == ':'
    assert es.statement.matrix(5).type == TokenType.Colon
    assert es.statement.matrix(6).text == '3==4?4:5'
    assert es.statement.matrix(6).type == TokenType.Statement
    assert es.statement.matrix(6, 0).text == '3'
    assert es.statement.matrix(6, 0).type == TokenType.RealNumber
    assert es.statement.matrix(6, 1).text == '=='
    assert es.statement.matrix(6, 1).type == TokenType.Eq
    assert es.statement.matrix(6, 2).text == '4'
    assert es.statement.matrix(6, 2).type == TokenType.RealNumber
    assert es.statement.matrix(6, 3).text == '?'
    assert es.statement.matrix(6, 3).type == TokenType.Question
    assert es.statement.matrix(6, 4).text == '4'
    assert es.statement.matrix(6, 4).type == TokenType.RealNumber
    assert es.statement.matrix(6, 5).text == ':'
    assert es.statement.matrix(6, 5).type == TokenType.Colon
    assert es.statement.matrix(6, 6).text == '5'
    assert es.statement.matrix(6, 6).type == TokenType.RealNumber


def case27():
    s = StringIO("a==1?true:(x==1?y:z)")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'a'
    assert es.statement.matrix(0).type == TokenType.Identifier
    assert es.statement.matrix(1).text == '=='
    assert es.statement.matrix(1).type == TokenType.Eq
    assert es.statement.matrix(2).text == '1'
    assert es.statement.matrix(2).type == TokenType.RealNumber
    assert es.statement.matrix(3).text == '?'
    assert es.statement.matrix(3).type == TokenType.Question
    assert es.statement.matrix(4).text == 'true'
    assert es.statement.matrix(4).type == TokenType.TRUE
    assert es.statement.matrix(5).text == ':'
    assert es.statement.matrix(5).type == TokenType.Colon
    assert es.statement.matrix(6).text == '(x==1?y:z)'
    assert es.statement.matrix(6).type == TokenType.Statement
    assert es.statement.matrix(6, 0).text == '(x==1?y:z)'
    assert es.statement.matrix(6, 0).type == TokenType.Statement
    assert es.statement.matrix(6, 0, 0).text == '('
    assert es.statement.matrix(6, 0, 0).type == TokenType.Lp
    assert es.statement.matrix(6, 0, 1).text == 'x==1?y:z'
    assert es.statement.matrix(6, 0, 1).type == TokenType.Statement
    assert es.statement.matrix(6, 0, 1, 0).text == 'x'
    assert es.statement.matrix(6, 0, 1, 0).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 1, 1).text == '=='
    assert es.statement.matrix(6, 0, 1, 1).type == TokenType.Eq
    assert es.statement.matrix(6, 0, 1, 2).text == '1'
    assert es.statement.matrix(6, 0, 1, 2).type == TokenType.RealNumber
    assert es.statement.matrix(6, 0, 1, 3).text == '?'
    assert es.statement.matrix(6, 0, 1, 3).type == TokenType.Question
    assert es.statement.matrix(6, 0, 1, 4).text == 'y'
    assert es.statement.matrix(6, 0, 1, 4).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 1, 5).text == ':'
    assert es.statement.matrix(6, 0, 1, 5).type == TokenType.Colon
    assert es.statement.matrix(6, 0, 1, 6).text == 'z'
    assert es.statement.matrix(6, 0, 1, 6).type == TokenType.Identifier
    assert es.statement.matrix(6, 0, 2).text == ')'
    assert es.statement.matrix(6, 0, 2).type == TokenType.Rp


def case28():
    s = StringIO("a(c())?1:b(d())")
    # s = StringIO("a?1:d(c())")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    es.statement.display([])
    assert es.statement.matrix(0).text == 'a(c())'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'a'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == 'c()'
    assert es.statement.matrix(0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0).text == 'c()'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 0).text == 'c'
    assert es.statement.matrix(0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '?'
    assert es.statement.matrix(1).type == TokenType.Question
    assert es.statement.matrix(2).text == '1'
    assert es.statement.matrix(2).type == TokenType.RealNumber
    assert es.statement.matrix(3).text == ':'
    assert es.statement.matrix(3).type == TokenType.Colon
    assert es.statement.matrix(4).text == 'b(d())'
    assert es.statement.matrix(4).type == TokenType.Statement
    assert es.statement.matrix(4, 0).text == 'b(d())'
    assert es.statement.matrix(4, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 0).text == 'b'
    assert es.statement.matrix(4, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 1).text == '('
    assert es.statement.matrix(4, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 0, 2).text == 'd()'
    assert es.statement.matrix(4, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 2, 0).text == 'd()'
    assert es.statement.matrix(4, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 2, 0, 0).text == 'd'
    assert es.statement.matrix(4, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(4, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 0, 2, 0, 2).text == ')'
    assert es.statement.matrix(4, 0, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(4, 0, 3).text == ')'
    assert es.statement.matrix(4, 0, 3).type == TokenType.Rp


def case29():
    s = StringIO("a(c())?1:b(d(1,2),x())")
    l = Lexer()
    l.tokenize(s)
    es = Parser(l.token_list)
    es.parse()
    assert es.statement.matrix(0).text == 'a(c())'
    assert es.statement.matrix(0).type == TokenType.Statement
    assert es.statement.matrix(0, 0).text == 'a'
    assert es.statement.matrix(0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 1).text == '('
    assert es.statement.matrix(0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2).text == 'c()'
    assert es.statement.matrix(0, 2).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0).text == 'c()'
    assert es.statement.matrix(0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(0, 2, 0, 0).text == 'c'
    assert es.statement.matrix(0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(0, 2, 0, 1).text == '('
    assert es.statement.matrix(0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(0, 2, 0, 2).text == ')'
    assert es.statement.matrix(0, 2, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(0, 3).text == ')'
    assert es.statement.matrix(0, 3).type == TokenType.Rp
    assert es.statement.matrix(1).text == '?'
    assert es.statement.matrix(1).type == TokenType.Question
    assert es.statement.matrix(2).text == '1'
    assert es.statement.matrix(2).type == TokenType.RealNumber
    assert es.statement.matrix(3).text == ':'
    assert es.statement.matrix(3).type == TokenType.Colon
    assert es.statement.matrix(4).text == 'b(d(1,2),x())'
    assert es.statement.matrix(4).type == TokenType.Statement
    assert es.statement.matrix(4, 0).text == 'b(d(1,2),x())'
    assert es.statement.matrix(4, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 0).text == 'b'
    assert es.statement.matrix(4, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 1).text == '('
    assert es.statement.matrix(4, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 0, 2).text == 'd(1,2)'
    assert es.statement.matrix(4, 0, 2).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 2, 0).text == 'd(1,2)'
    assert es.statement.matrix(4, 0, 2, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 2, 0, 0).text == 'd'
    assert es.statement.matrix(4, 0, 2, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 2, 0, 1).text == '('
    assert es.statement.matrix(4, 0, 2, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 0, 2, 0, 2).text == '1'
    assert es.statement.matrix(4, 0, 2, 0, 2).type == TokenType.RealNumber
    assert es.statement.matrix(4, 0, 2, 0, 3).text == ','
    assert es.statement.matrix(4, 0, 2, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(4, 0, 2, 0, 4).text == '2'
    assert es.statement.matrix(4, 0, 2, 0, 4).type == TokenType.RealNumber
    assert es.statement.matrix(4, 0, 2, 0, 5).text == ')'
    assert es.statement.matrix(4, 0, 2, 0, 5).type == TokenType.Rp
    assert es.statement.matrix(4, 0, 3).text == ','
    assert es.statement.matrix(4, 0, 3).type == TokenType.Comma
    assert es.statement.matrix(4, 0, 4).text == 'x()'
    assert es.statement.matrix(4, 0, 4).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 4, 0).text == 'x()'
    assert es.statement.matrix(4, 0, 4, 0).type == TokenType.Statement
    assert es.statement.matrix(4, 0, 4, 0, 0).text == 'x'
    assert es.statement.matrix(4, 0, 4, 0, 0).type == TokenType.Identifier
    assert es.statement.matrix(4, 0, 4, 0, 1).text == '('
    assert es.statement.matrix(4, 0, 4, 0, 1).type == TokenType.Lp
    assert es.statement.matrix(4, 0, 4, 0, 2).text == ')'
    assert es.statement.matrix(4, 0, 4, 0, 2).type == TokenType.Rp
    assert es.statement.matrix(4, 0, 5).text == ')'
    assert es.statement.matrix(4, 0, 5).type == TokenType.Rp


# def test_cases2():
#     case27()


def test_cases():
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
    case18()
    case19()
    case20()
    case21()
    case24()
    case25()
    case26()
    case27()
    case28()
    case29()
