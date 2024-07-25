from io import StringIO

import pytest

from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.token_type import TokenType


def test_lexer():
    lexer = Lexer()
    identifier_token(lexer)
    true_token(lexer)
    blank_token_with_ture_false(lexer)
    blank_token_with_id(lexer)
    comma_with_true_false(lexer)
    byte_and_token(lexer)
    and_token(lexer)
    byte_or_token(lexer)
    or_token(lexer)
    real_number_token(lexer)
    plus_token(lexer)
    minus_token(lexer)
    d_plus_token(lexer)
    d_minus_token(lexer)
    complex_expression(lexer)
    plus_eq_token(lexer)
    minus_eq_token(lexer)
    colon_token(lexer)
    sq_token(lexer)
    dq_token(lexer)
    comma_token(lexer)
    question_token(lexer)
    lp_rp_token(lexer)
    test_vars()
    test_ge_and_gt()
    neq()
    le_and_lt()
    assign()
    eq_plus()
    eq_minus()
    aways_eq_plus()
    mul_and_divide()
    test_math_name()



def identifier_token(lexer: Lexer):
    string = StringIO("t")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "t"
    string = StringIO("tr")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "tr"
    string = StringIO("tru")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "tru"
    string = StringIO("trua")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "trua"
    string = StringIO("f")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "f"
    string = StringIO("fa")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "fa"
    string = StringIO("fal")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "fal"
    string = StringIO("fals")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "fals"
    string = StringIO("falsg")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "falsg"
    string = StringIO("aaaa1111")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "aaaa1111"


def true_token(lexer: Lexer):
    string = StringIO("true")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    string = StringIO("abcdtrue")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "abcdtrue"
    string = StringIO("abcdtrus")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "abcdtrus"
    string = StringIO("true111")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "true111"


def false_token(lexer: Lexer):
    string = StringIO("false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.FALSE
    assert lexer.token_list[0].text == "false"
    string = StringIO("falseaasds")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "falseaasds"


def blank_token_with_id(lexer: Lexer):
    string = StringIO("a b")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "b"


def blank_token_with_ture_false(lexer: Lexer):
    string = StringIO("true false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.FALSE
    assert lexer.token_list[2].text == "false"
    string = StringIO("true xxxxxxxxxx false false ")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "xxxxxxxxxx"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    assert lexer.token_list[5].type == TokenType.Blank
    assert lexer.token_list[5].text == " "
    assert lexer.token_list[6].type == TokenType.FALSE
    assert lexer.token_list[6].text == "false"
    string = StringIO("true xxxxxxxxxx false true ")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "xxxxxxxxxx"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    assert lexer.token_list[5].type == TokenType.Blank
    assert lexer.token_list[5].text == " "
    assert lexer.token_list[6].type == TokenType.TRUE
    assert lexer.token_list[6].text == "true"


def byte_and_token(lexer: Lexer):
    string = StringIO("&")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.ByteAnd
    assert lexer.token_list[0].text == "&"
    string = StringIO("true & false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.ByteAnd
    assert lexer.token_list[2].text == "&"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    string = StringIO("true&false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.ByteAnd
    assert lexer.token_list[1].text == "&"
    assert lexer.token_list[2].type == TokenType.FALSE
    assert lexer.token_list[2].text == "false"
    string = StringIO("true&fgggg")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.ByteAnd
    assert lexer.token_list[1].text == "&"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "fgggg"


def comma_with_true_false(lexer: Lexer):
    string = StringIO("true,false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[1].type == TokenType.Comma
    assert lexer.token_list[2].type == TokenType.FALSE

def and_token(lexer: Lexer):
    string = StringIO("&&")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.And
    assert lexer.token_list[0].text == "&&"
    string = StringIO("true&&false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.And
    assert lexer.token_list[1].text == "&&"
    assert lexer.token_list[2].type == TokenType.FALSE
    assert lexer.token_list[2].text == "false"
    string = StringIO("true && false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.And
    assert lexer.token_list[2].text == "&&"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    string = StringIO("true&&fgggg")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.And
    assert lexer.token_list[1].text == "&&"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "fgggg"


def byte_or_token(lexer: Lexer):
    string = StringIO("|")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.ByteOr
    assert lexer.token_list[0].text == "|"
    string = StringIO("true | false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.ByteOr
    assert lexer.token_list[2].text == "|"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    string = StringIO("true|false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.ByteOr
    assert lexer.token_list[1].text == "|"
    assert lexer.token_list[2].type == TokenType.FALSE
    assert lexer.token_list[2].text == "false"
    string = StringIO("true|fgggg")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.ByteOr
    assert lexer.token_list[1].text == "|"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "fgggg"


def or_token(lexer: Lexer):
    string = StringIO("||")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Or
    assert lexer.token_list[0].text == "||"
    string = StringIO("true || false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.Or
    assert lexer.token_list[2].text == "||"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    string = StringIO("true||false")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Or
    assert lexer.token_list[1].text == "||"
    assert lexer.token_list[2].type == TokenType.FALSE
    assert lexer.token_list[2].text == "false"
    string = StringIO("true||fgggg")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.TRUE
    assert lexer.token_list[0].text == "true"
    assert lexer.token_list[1].type == TokenType.Or
    assert lexer.token_list[1].text == "||"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "fgggg"


def real_number_token(lexer: Lexer):
    string = StringIO("1")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    string = StringIO("1.2")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1.2"
    string = StringIO("xxx 1.2 true")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "xxx"
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1.2"
    assert lexer.token_list[3].type == TokenType.Blank
    assert lexer.token_list[3].text == " "
    assert lexer.token_list[4].type == TokenType.TRUE
    assert lexer.token_list[4].text == "true"
    string = StringIO("0.10")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "0.10"
    with pytest.raises(Exception):
        string = StringIO("xxx 1. true")
        lexer.tokenize(string)


def plus_token(lexer: Lexer):
    string = StringIO("1+2")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.Plus
    assert lexer.token_list[1].text == "+"
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "2"
    string = StringIO("1+aaaaa")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.Plus
    assert lexer.token_list[1].text == "+"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "aaaaa"
    string = StringIO("+")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Plus
    assert lexer.token_list[0].text == "+"


def minus_token(lexer: Lexer):
    string = StringIO("1-2")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.Minus
    assert lexer.token_list[1].text == "-"
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "2"
    string = StringIO("1-aaaaa")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.Minus
    assert lexer.token_list[1].text == "-"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "aaaaa"
    string = StringIO("-")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Minus
    assert lexer.token_list[0].text == "-"


def d_plus_token(lexer: Lexer):
    string = StringIO("++")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.DPlus
    assert lexer.token_list[0].text == "++"
    string = StringIO("1++")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.DPlus
    assert lexer.token_list[1].text == "++"

    string = StringIO("a++")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.DPlus
    assert lexer.token_list[1].text == "++"

    string = StringIO("a++b")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.DPlus
    assert lexer.token_list[1].text == "++"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "b"


def d_minus_token(lexer: Lexer):
    string = StringIO("--")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.DMinus
    assert lexer.token_list[0].text == "--"
    string = StringIO("1--")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.DMinus
    assert lexer.token_list[1].text == "--"

    string = StringIO("a--")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.DMinus
    assert lexer.token_list[1].text == "--"

    string = StringIO("a--b")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.DMinus
    assert lexer.token_list[1].text == "--"
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "b"


def complex_expression(lexer: Lexer):
    string = StringIO("1++1+aa1s-d-- ")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.DPlus
    assert lexer.token_list[1].text == "++"
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1"
    assert lexer.token_list[3].type == TokenType.Plus
    assert lexer.token_list[3].text == "+"
    assert lexer.token_list[4].type == TokenType.Identifier
    assert lexer.token_list[4].text == "aa1s"
    assert lexer.token_list[5].type == TokenType.Minus
    assert lexer.token_list[5].text == "-"
    assert lexer.token_list[6].type == TokenType.Identifier
    assert lexer.token_list[6].text == "d"
    assert lexer.token_list[7].type == TokenType.DMinus
    assert lexer.token_list[7].text == "--"


def plus_eq_token(lexer: Lexer):
    string = StringIO("+=")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.PlusEq
    assert lexer.token_list[0].text == "+="
    string = StringIO("a+=1")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.PlusEq
    assert lexer.token_list[1].text == "+="
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1"


def minus_eq_token(lexer: Lexer):
    string = StringIO("-=")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.MinusEq
    assert lexer.token_list[0].text == "-="
    string = StringIO("a-=1")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.MinusEq
    assert lexer.token_list[1].text == "-="
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1"


def colon_token(lexer: Lexer):
    string = StringIO(":")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Colon
    assert lexer.token_list[0].text == ":"
    string = StringIO("1:1")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.RealNumber
    assert lexer.token_list[0].text == "1"
    assert lexer.token_list[1].type == TokenType.Colon
    assert lexer.token_list[1].text == ":"
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1"
    string = StringIO(":1+1:1++:ad:true:false:")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Colon
    assert lexer.token_list[0].text == ":"
    assert lexer.token_list[1].type == TokenType.RealNumber
    assert lexer.token_list[1].text == "1"
    assert lexer.token_list[2].type == TokenType.Plus
    assert lexer.token_list[2].text == "+"
    assert lexer.token_list[3].type == TokenType.RealNumber
    assert lexer.token_list[3].text == "1"
    assert lexer.token_list[4].type == TokenType.Colon
    assert lexer.token_list[4].text == ":"
    assert lexer.token_list[5].type == TokenType.RealNumber
    assert lexer.token_list[5].text == "1"
    assert lexer.token_list[6].type == TokenType.DPlus
    assert lexer.token_list[6].text == "++"

    assert lexer.token_list[7].type == TokenType.Colon
    assert lexer.token_list[7].text == ":"
    assert lexer.token_list[8].type == TokenType.Identifier
    assert lexer.token_list[8].text == "ad"
    assert lexer.token_list[9].type == TokenType.Colon
    assert lexer.token_list[9].text == ":"
    assert lexer.token_list[10].type == TokenType.TRUE
    assert lexer.token_list[10].text == "true"
    assert lexer.token_list[11].type == TokenType.Colon
    assert lexer.token_list[11].text == ":"
    assert lexer.token_list[12].type == TokenType.FALSE
    assert lexer.token_list[12].text == "false"
    assert lexer.token_list[13].type == TokenType.Colon
    assert lexer.token_list[13].text == ":"


def sq_token(lexer: Lexer):
    string = StringIO("':1+1:1++:'ad:true:false:")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "':1+1:1++:'ad"
    assert lexer.token_list[1].type == TokenType.Colon
    assert lexer.token_list[1].text == ":"
    assert lexer.token_list[2].type == TokenType.TRUE
    assert lexer.token_list[2].text == "true"
    assert lexer.token_list[3].type == TokenType.Colon
    assert lexer.token_list[3].text == ":"
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    string = StringIO("'true:false'")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "'true:false'"
    string = StringIO("'false:true'+1")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "'false:true'"
    assert lexer.token_list[1].type == TokenType.Plus
    assert lexer.token_list[1].text == "+"
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1"
    string = StringIO("' '")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "' '"


def dq_token(lexer: Lexer):
    string = StringIO("\":1+1:1++:\"ad:true:false:")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "\":1+1:1++:\"ad"
    assert lexer.token_list[1].type == TokenType.Colon
    assert lexer.token_list[1].text == ":"
    assert lexer.token_list[2].type == TokenType.TRUE
    assert lexer.token_list[2].text == "true"
    assert lexer.token_list[3].type == TokenType.Colon
    assert lexer.token_list[3].text == ":"
    assert lexer.token_list[4].type == TokenType.FALSE
    assert lexer.token_list[4].text == "false"
    string = StringIO("\"true:false\"")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "\"true:false\""
    string = StringIO("\"false:true\"+1")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "\"false:true\""
    assert lexer.token_list[1].type == TokenType.Plus
    assert lexer.token_list[1].text == "+"
    assert lexer.token_list[2].type == TokenType.RealNumber
    assert lexer.token_list[2].text == "1"
    string = StringIO("\" \"")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "\" \""


def question_token(lexer: Lexer):
    string = StringIO("?")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Question
    assert lexer.token_list[0].text == "?"
    string = StringIO("a:?b")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[0].text == "a"
    assert lexer.token_list[1].type == TokenType.Colon
    assert lexer.token_list[1].text == ":"
    assert lexer.token_list[2].type == TokenType.Question
    assert lexer.token_list[2].text == "?"
    assert lexer.token_list[3].type == TokenType.Identifier
    assert lexer.token_list[3].text == "b"
    # string = StringIO("a = 1? c:d")
    # lexer.tokenize(string)
    # assert lexer.token_list[0].type == TokenType.Identifier
    # assert lexer.token_list[0].text == "a"
    # assert lexer.token_list[1].type == TokenType.Blank
    # assert lexer.token_list[1].text == " "
    # assert lexer.token_list[2].type == TokenType.Assignment
    # assert lexer.token_list[2].text == "="
    # assert lexer.token_list[3].type == TokenType.Blank
    # assert lexer.token_list[3].text == " "


def comma_token(lexer: Lexer):
    string = StringIO(",")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Comma
    assert lexer.token_list[0].text == ","
    string = StringIO(", +,")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Comma
    assert lexer.token_list[0].text == ","
    assert lexer.token_list[1].type == TokenType.Blank
    assert lexer.token_list[1].text == " "
    assert lexer.token_list[2].type == TokenType.Plus
    assert lexer.token_list[2].text == "+"
    assert lexer.token_list[3].type == TokenType.Comma
    assert lexer.token_list[3].text == ","


def lp_rp_token(lexer: Lexer):
    string = StringIO("()")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Lp
    assert lexer.token_list[0].text == "("
    assert lexer.token_list[1].type == TokenType.Rp
    assert lexer.token_list[1].text == ")"

    string = StringIO("(1+2)")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Lp
    assert lexer.token_list[0].text == "("
    assert lexer.token_list[1].type == TokenType.RealNumber
    assert lexer.token_list[1].text == "1"
    assert lexer.token_list[2].type == TokenType.Plus
    assert lexer.token_list[2].text == "+"
    assert lexer.token_list[3].type == TokenType.RealNumber
    assert lexer.token_list[3].text == "2"
    assert lexer.token_list[4].type == TokenType.Rp
    assert lexer.token_list[4].text == ")"

    string = StringIO("(\"ass\" + \"1+2\")")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Lp
    assert lexer.token_list[0].text == "("
    assert lexer.token_list[1].type == TokenType.Identifier
    assert lexer.token_list[1].text == "\"ass\""
    assert lexer.token_list[2].type == TokenType.Blank
    assert lexer.token_list[2].text == " "
    assert lexer.token_list[3].type == TokenType.Plus
    assert lexer.token_list[3].text == "+"
    assert lexer.token_list[4].type == TokenType.Blank
    assert lexer.token_list[4].text == " "
    assert lexer.token_list[5].type == TokenType.Identifier
    assert lexer.token_list[5].text == "\"1+2\""
    assert lexer.token_list[6].type == TokenType.Rp
    assert lexer.token_list[6].text == ")"
    string = StringIO("('ass' + '1+2')")
    lexer.tokenize(string)
    assert lexer.token_list[0].type == TokenType.Lp
    assert lexer.token_list[0].text == "("
    assert lexer.token_list[1].type == TokenType.Identifier
    assert lexer.token_list[1].text == "'ass'"
    assert lexer.token_list[2].type == TokenType.Blank
    assert lexer.token_list[2].text == " "
    assert lexer.token_list[3].type == TokenType.Plus
    assert lexer.token_list[3].text == "+"
    assert lexer.token_list[4].type == TokenType.Blank
    assert lexer.token_list[4].text == " "
    assert lexer.token_list[5].type == TokenType.Identifier
    assert lexer.token_list[5].text == "'1+2'"
    assert lexer.token_list[6].type == TokenType.Rp
    assert lexer.token_list[6].text == ")"


def test_ge_and_gt():
    s1 = StringIO("dateDiff(getMinByLog($ *.InformedConsent.DSSTDAT), $ *.*.*, \"D\") > tt: true")
    l = Lexer()
    l.tokenize(s1)
    assert l.token_list[14].type == TokenType.Gt
    assert l.token_list[14].text == ">"
    assert "".join([token.text for token in l.token_list]) == s1.getvalue()
    s2 = StringIO("dateDiff(getMinByLog($ *.InformedConsent.DSSTDAT), $ *.*.*, \"D\")>=0: true")
    lexer = Lexer()
    lexer.tokenize(s2)
    assert lexer.token_list[13].type == TokenType.Ge
    assert lexer.token_list[13].text == ">="
    assert "".join([token.text for token in lexer.token_list]) == s2.getvalue()


def le_and_lt():
    s1 = StringIO("dateDiff(getMinByLog($ *.InformedConsent.DSSTDAT), $ *.*.*, \"D\") < tt: true")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[14].type == TokenType.Lt
    assert lexer.token_list[14].text == "<"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s2 = StringIO("dateDiff(getMinByLog($ *.InformedConsent.DSSTDAT), $ *.*.*, \"D\")<=0: true")
    lexer = Lexer()
    lexer.tokenize(s2)
    assert "".join([token.text for token in lexer.token_list]) == s2.getvalue()
    assert lexer.token_list[13].type == TokenType.Le
    assert lexer.token_list[13].text == "<="


def neq():
    s1 = StringIO("toDate($*.*.*)!=""&&toDate(getMinByLog($*.Informed Consent.DSSTDAT))")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[4].type == TokenType.NEq
    assert lexer.token_list[4].text == "!="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("toDate($*.*.*)!==""&&toDate(getMinByLog($*.Informed Consent.DSSTDAT))")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[4].type == TokenType.Nidentity
    assert lexer.token_list[4].text == "!=="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()


def assign():
    s1 = StringIO("a=1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[1].type == TokenType.Assignment
    assert lexer.token_list[1].text == "="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a=1)")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.Assignment
    assert lexer.token_list[2].text == "="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a=1)&&b=1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.Assignment
    assert lexer.token_list[7].type == TokenType.Assignment
    assert lexer.token_list[2].text == "="
    assert lexer.token_list[7].text == "="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()


def eq():
    s1 = StringIO("a==1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[1].type == TokenType.Eq
    assert lexer.token_list[1].text == "=="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a==1)")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.Eq
    assert lexer.token_list[2].text == "=="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a==1)&&b==1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.Eq
    assert lexer.token_list[7].type == TokenType.Eq
    assert lexer.token_list[2].text == "=="
    assert lexer.token_list[7].text == "=="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()


def eq_plus():
    s1 = StringIO("a=+1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[1].type == TokenType.EqPlus
    assert lexer.token_list[1].text == "=+"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a=+1)")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.EqPlus
    assert lexer.token_list[2].text == "=+"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a=+1)&&b=+1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.EqPlus
    assert lexer.token_list[7].type == TokenType.EqPlus
    assert lexer.token_list[2].text == "=+"
    assert lexer.token_list[7].text == "=+"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()


def eq_minus():
    s1 = StringIO("a=-1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[1].type == TokenType.EqMinus
    assert lexer.token_list[1].text == "=-"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a=-1)")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.EqMinus
    assert lexer.token_list[2].text == "=-"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a=-1)&&b=-1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.EqMinus
    assert lexer.token_list[7].type == TokenType.EqMinus
    assert lexer.token_list[2].text == "=-"
    assert lexer.token_list[7].text == "=-"
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()


def aways_eq_plus():
    s1 = StringIO("a===1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[1].type == TokenType.AwaysEq
    assert lexer.token_list[1].text == "==="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a===1)")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.AwaysEq
    assert lexer.token_list[2].text == "==="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()
    s1 = StringIO("(a===1)&&b===1")
    lexer = Lexer()
    lexer.tokenize(s1)
    assert lexer.token_list[2].type == TokenType.AwaysEq
    assert lexer.token_list[7].type == TokenType.AwaysEq
    assert lexer.token_list[2].text == "==="
    assert lexer.token_list[7].text == "==="
    assert "".join([token.text for token in lexer.token_list]) == s1.getvalue()


def mul_and_divide():
    string = StringIO("toNum($*.*.EGORRES.881)/1000")
    lexer = Lexer()
    lexer.tokenize(string)

    assert "".join([token.text for token in lexer.token_list]) == string.getvalue()
    string = StringIO("toNum($*.*.EGORRES.881)*1000")
    lexer = Lexer()
    lexer.tokenize(string)

    assert "".join([token.text for token in lexer.token_list]) == string.getvalue()



def test_vars():
    s = StringIO("$*.*.EGPERF==\"Y\"")
    lexer = Lexer()
    lexer.tokenize(s)
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[0].text == "$*.*.EGPERF"
    assert lexer.token_list[1].type == TokenType.Eq
    assert lexer.token_list[1].text == "=="
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[2].text == "\"Y\""
    s = StringIO("$C1D1.ONC-392 Administration.ECSTTIM+\":00\"")
    lexer = Lexer()
    lexer.tokenize(s)
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[1].type == TokenType.Plus
    assert lexer.token_list[2].type == TokenType.Identifier
    s = StringIO("$*.*.*>=\":00\"")
    lexer = Lexer()
    lexer.tokenize(s)
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[1].type == TokenType.Ge
    assert lexer.token_list[2].type == TokenType.Identifier
    s = StringIO("$C1D1.ONC-392 Administration.ECSTTIM.1992+\":00\"")
    lexer = Lexer()
    lexer.tokenize(s)
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[1].type == TokenType.Plus
    assert lexer.token_list[2].type == TokenType.Identifier
    s = StringIO("$*.*.*.1992")
    lexer = Lexer()
    lexer.tokenize(s)
    assert lexer.token_list[0].type == TokenType.Variable
    s = StringIO("$*.*.*.1992>=\":00\"")
    lexer = Lexer()
    lexer.tokenize(s)
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[1].type == TokenType.Ge
    assert lexer.token_list[2].type == TokenType.Identifier


def test_math_name():
    s = StringIO("Math.power()")
    l = Lexer()
    l.tokenize(s)
    print(l.token_list)



