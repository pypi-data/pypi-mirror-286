from io import StringIO

import pytest

from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.lexer.token_type import TokenType


@pytest.fixture
def rules():
    return [
        """toDate($*.*.*)!=""&&toDate(getMinByLog($*.Informed Consent.DSSTDAT))!=""?dateDiff(getMinByLog($*.Informed Consent.DSSTDAT),$*.*.*, "D")>0:true""",
        """isValidDate($*.*.*)""",
        """autoValue((toNum($*.*.EGORRES.881)!=''&&toNum($*.*.EGORRES.879)!=''?RoundN(toNum($*.*.EGORRES.879)/Math.pow((toNum($*.*.EGORRES.881)/1000), 0.33), "1"):""), true)""",
        "$*.*.EGPERF==\"Y\"",
        "$*.*.EGORRES.12394==\"CS\"",
        """condition(mustAnswer(toNum($*.*.*)), isRange($*.*.*, 40,160))""",
        """mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='Y'?$*.*.*=='':true""",
        """mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'?$*.*.*!='':true""",
        """autoIncrease(1,1,1,1)""",
        """$*.*.*=='Y'&&mustAnswer($*.Demographics.AGE)?toNum($*.Demographics.AGE)>=18:true""",
        """mustAnswer($*.*.*)&&(getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)=='V1.5'||getICFVersion($*.Date of Visit.SVDAT, $*.Informed Consent.DSSTDAT, $*.Informed Consent.VERSION)=='V1.6')?($*.*.*=='0'||$*.*.*=='1'||$*.*.*=='2'):true""",
        """toDate($C1D1.ONC-392 Administration.ECSTDAT)!=""&& toDate($*.*.LBDAT)!=""&& toDate("2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00")!="" &&toDate("2015-1-12 "+$*.*.*+":00")!=""?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0:true""",
        """autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01), true)"""
    ]


def test_rule(rules):
    test_rule_lexer0(rules=rules)
    test_rule_lexer1(rules=rules)
    test_rule_lexer2(rules=rules)
    test_rule_lexer3(rules=rules)
    test_rule_lexer4(rules=rules)
    test_rule_lexer5(rules=rules)
    test_rule_lexer6(rules=rules)
    test_rule_lexer7(rules=rules)
    test_rule_lexer8(rules=rules)
    test_rule_lexer9(rules=rules)
    test_rule_lexer10(rules=rules)
    test_rule_lexer11(rules=rules)
    test_rule_lexer12(rules=rules)





def test_rule_lexer0(rules):
    string = StringIO(rules[0])
    lexer = Lexer()
    lexer.tokenize(string)
    assert lexer.token_list[0].text == 'toDate'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == '$*.*.*'
    assert lexer.token_list[2].type == TokenType.Variable
    assert lexer.token_list[3].text == ')'
    assert lexer.token_list[3].type == TokenType.Rp
    assert lexer.token_list[4].text == '!='
    assert lexer.token_list[4].type == TokenType.NEq
    assert lexer.token_list[5].text == '""'
    assert lexer.token_list[5].type == TokenType.Identifier
    assert lexer.token_list[6].text == '&&'
    assert lexer.token_list[6].type == TokenType.And
    assert lexer.token_list[7].text == 'toDate'
    assert lexer.token_list[7].type == TokenType.Identifier
    assert lexer.token_list[8].text == '('
    assert lexer.token_list[8].type == TokenType.Lp
    assert lexer.token_list[9].text == 'getMinByLog'
    assert lexer.token_list[9].type == TokenType.Identifier
    assert lexer.token_list[10].text == '('
    assert lexer.token_list[10].type == TokenType.Lp
    assert lexer.token_list[11].text == '$*.Informed Consent.DSSTDAT'
    assert lexer.token_list[11].type == TokenType.Variable
    assert lexer.token_list[12].text == ')'
    assert lexer.token_list[12].type == TokenType.Rp
    assert lexer.token_list[13].text == ')'
    assert lexer.token_list[13].type == TokenType.Rp
    assert lexer.token_list[14].text == '!='
    assert lexer.token_list[14].type == TokenType.NEq
    assert lexer.token_list[15].text == '""'
    assert lexer.token_list[15].type == TokenType.Identifier
    assert lexer.token_list[16].text == '?'
    assert lexer.token_list[16].type == TokenType.Question
    assert lexer.token_list[17].text == 'dateDiff'
    assert lexer.token_list[17].type == TokenType.Identifier
    assert lexer.token_list[18].text == '('
    assert lexer.token_list[18].type == TokenType.Lp
    assert lexer.token_list[19].text == 'getMinByLog'
    assert lexer.token_list[19].type == TokenType.Identifier
    assert lexer.token_list[20].text == '('
    assert lexer.token_list[20].type == TokenType.Lp
    assert lexer.token_list[21].text == '$*.Informed Consent.DSSTDAT'
    assert lexer.token_list[21].type == TokenType.Variable
    assert lexer.token_list[22].text == ')'
    assert lexer.token_list[22].type == TokenType.Rp
    assert lexer.token_list[23].text == ','
    assert lexer.token_list[23].type == TokenType.Comma
    assert lexer.token_list[24].text == '$*.*.*'
    assert lexer.token_list[24].type == TokenType.Variable
    assert lexer.token_list[25].text == ','
    assert lexer.token_list[25].type == TokenType.Comma
    assert lexer.token_list[26].text == ' '
    assert lexer.token_list[26].type == TokenType.Blank
    assert lexer.token_list[27].text == '"D"'
    assert lexer.token_list[27].type == TokenType.Identifier
    assert lexer.token_list[28].text == ')'
    assert lexer.token_list[28].type == TokenType.Rp
    assert lexer.token_list[29].text == '>'
    assert lexer.token_list[29].type == TokenType.Gt
    assert lexer.token_list[30].text == '0'
    assert lexer.token_list[30].type == TokenType.RealNumber
    assert lexer.token_list[31].text == ':'
    assert lexer.token_list[31].type == TokenType.Colon
    assert lexer.token_list[32].text == 'true'
    assert lexer.token_list[32].type == TokenType.TRUE
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer1(rules):
    string = StringIO(rules[1])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == 'isValidDate'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == '$*.*.*'
    assert lexer.token_list[2].type == TokenType.Variable
    assert lexer.token_list[3].text == ')'
    assert lexer.token_list[3].type == TokenType.Rp

    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer2(rules):
    string = StringIO(rules[2])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == 'autoValue'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == '('
    assert lexer.token_list[2].type == TokenType.Lp
    assert lexer.token_list[3].text == 'toNum'
    assert lexer.token_list[3].type == TokenType.Identifier
    assert lexer.token_list[4].text == '('
    assert lexer.token_list[4].type == TokenType.Lp
    assert lexer.token_list[5].text == '$*.*.EGORRES.881'
    assert lexer.token_list[5].type == TokenType.Variable
    assert lexer.token_list[6].text == ')'
    assert lexer.token_list[6].type == TokenType.Rp
    assert lexer.token_list[7].text == '!='
    assert lexer.token_list[7].type == TokenType.NEq
    assert lexer.token_list[8].text == '\'\''
    assert lexer.token_list[8].type == TokenType.Identifier
    assert lexer.token_list[9].text == '&&'
    assert lexer.token_list[9].type == TokenType.And
    assert lexer.token_list[10].text == 'toNum'
    assert lexer.token_list[10].type == TokenType.Identifier
    assert lexer.token_list[11].text == '('
    assert lexer.token_list[11].type == TokenType.Lp
    assert lexer.token_list[12].text == '$*.*.EGORRES.879'
    assert lexer.token_list[12].type == TokenType.Variable
    assert lexer.token_list[13].text == ')'
    assert lexer.token_list[13].type == TokenType.Rp
    assert lexer.token_list[14].text == '!='
    assert lexer.token_list[14].type == TokenType.NEq
    assert lexer.token_list[15].text == '\'\''
    assert lexer.token_list[15].type == TokenType.Identifier
    assert lexer.token_list[16].text == '?'
    assert lexer.token_list[16].type == TokenType.Question
    assert lexer.token_list[17].text == 'RoundN'
    assert lexer.token_list[17].type == TokenType.Identifier
    assert lexer.token_list[18].text == '('
    assert lexer.token_list[18].type == TokenType.Lp
    assert lexer.token_list[19].text == 'toNum'
    assert lexer.token_list[19].type == TokenType.Identifier
    assert lexer.token_list[20].text == '('
    assert lexer.token_list[20].type == TokenType.Lp
    assert lexer.token_list[21].text == '$*.*.EGORRES.879'
    assert lexer.token_list[21].type == TokenType.Variable
    assert lexer.token_list[22].text == ')'
    assert lexer.token_list[22].type == TokenType.Rp
    assert lexer.token_list[23].text == '/'
    assert lexer.token_list[23].type == TokenType.Divide
    assert lexer.token_list[24].text == 'Math.pow'
    assert lexer.token_list[24].type == TokenType.Identifier
    assert lexer.token_list[25].text == '('
    assert lexer.token_list[25].type == TokenType.Lp
    assert lexer.token_list[26].text == '('
    assert lexer.token_list[26].type == TokenType.Lp
    assert lexer.token_list[27].text == 'toNum'
    assert lexer.token_list[27].type == TokenType.Identifier
    assert lexer.token_list[28].text == '('
    assert lexer.token_list[28].type == TokenType.Lp
    assert lexer.token_list[29].text == '$*.*.EGORRES.881'
    assert lexer.token_list[29].type == TokenType.Variable
    assert lexer.token_list[30].text == ')'
    assert lexer.token_list[30].type == TokenType.Rp
    assert lexer.token_list[31].text == '/'
    assert lexer.token_list[31].type == TokenType.Divide
    assert lexer.token_list[32].text == '1000'
    assert lexer.token_list[32].type == TokenType.RealNumber
    assert lexer.token_list[33].text == ')'
    assert lexer.token_list[33].type == TokenType.Rp
    assert lexer.token_list[34].text == ','
    assert lexer.token_list[34].type == TokenType.Comma
    assert lexer.token_list[35].text == ' '
    assert lexer.token_list[35].type == TokenType.Blank
    assert lexer.token_list[36].text == '0.33'
    assert lexer.token_list[36].type == TokenType.RealNumber
    assert lexer.token_list[37].text == ')'
    assert lexer.token_list[37].type == TokenType.Rp
    assert lexer.token_list[38].text == ','
    assert lexer.token_list[38].type == TokenType.Comma
    assert lexer.token_list[39].text == ' '
    assert lexer.token_list[39].type == TokenType.Blank
    assert lexer.token_list[40].text == '"1"'
    assert lexer.token_list[40].type == TokenType.Identifier
    assert lexer.token_list[41].text == ')'
    assert lexer.token_list[41].type == TokenType.Rp
    assert lexer.token_list[42].text == ':'
    assert lexer.token_list[42].type == TokenType.Colon
    assert lexer.token_list[43].text == '""'
    assert lexer.token_list[43].type == TokenType.Identifier
    assert lexer.token_list[44].text == ')'
    assert lexer.token_list[44].type == TokenType.Rp
    assert lexer.token_list[45].text == ','
    assert lexer.token_list[45].type == TokenType.Comma
    assert lexer.token_list[46].text == ' '
    assert lexer.token_list[46].type == TokenType.Blank
    assert lexer.token_list[47].text == 'true'
    assert lexer.token_list[47].type == TokenType.TRUE
    assert lexer.token_list[48].text == ')'
    assert lexer.token_list[48].type == TokenType.Rp

    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer3(rules):
    string = StringIO(rules[3])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == '$*.*.EGPERF'
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[1].text == '=='
    assert lexer.token_list[1].type == TokenType.Eq
    assert lexer.token_list[2].text == '"Y"'
    assert lexer.token_list[2].type == TokenType.Identifier


    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer4(rules):
    string = StringIO(rules[4])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == '$*.*.EGORRES.12394'
    assert lexer.token_list[0].type == TokenType.Variable
    assert lexer.token_list[1].text == '=='
    assert lexer.token_list[1].type == TokenType.Eq
    assert lexer.token_list[2].text == '"CS"'
    assert lexer.token_list[2].type == TokenType.Identifier
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer5(rules):
    string = StringIO(rules[5])
    lexer = Lexer()
    lexer.tokenize(string)
    assert lexer.token_list[0].text == 'condition'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == 'mustAnswer'
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[3].text == '('
    assert lexer.token_list[3].type == TokenType.Lp
    assert lexer.token_list[4].text == 'toNum'
    assert lexer.token_list[4].type == TokenType.Identifier
    assert lexer.token_list[5].text == '('
    assert lexer.token_list[5].type == TokenType.Lp
    assert lexer.token_list[6].text == '$*.*.*'
    assert lexer.token_list[6].type == TokenType.Variable
    assert lexer.token_list[7].text == ')'
    assert lexer.token_list[7].type == TokenType.Rp
    assert lexer.token_list[8].text == ')'
    assert lexer.token_list[8].type == TokenType.Rp
    assert lexer.token_list[9].text == ','
    assert lexer.token_list[9].type == TokenType.Comma
    assert lexer.token_list[10].text == ' '
    assert lexer.token_list[10].type == TokenType.Blank
    assert lexer.token_list[11].text == 'isRange'
    assert lexer.token_list[11].type == TokenType.Identifier
    assert lexer.token_list[12].text == '('
    assert lexer.token_list[12].type == TokenType.Lp
    assert lexer.token_list[13].text == '$*.*.*'
    assert lexer.token_list[13].type == TokenType.Variable
    assert lexer.token_list[14].text == ','
    assert lexer.token_list[14].type == TokenType.Comma
    assert lexer.token_list[15].text == ' '
    assert lexer.token_list[15].type == TokenType.Blank
    assert lexer.token_list[16].text == '40'
    assert lexer.token_list[16].type == TokenType.RealNumber
    assert lexer.token_list[17].text == ','
    assert lexer.token_list[17].type == TokenType.Comma
    assert lexer.token_list[18].text == '160'
    assert lexer.token_list[18].type == TokenType.RealNumber
    assert lexer.token_list[19].text == ')'
    assert lexer.token_list[19].type == TokenType.Rp
    assert lexer.token_list[20].text == ')'
    assert lexer.token_list[20].type == TokenType.Rp

    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer6(rules):
    string = StringIO(rules[6])
    lexer = Lexer()
    lexer.tokenize(string)
    assert lexer.token_list[0].text == 'mustAnswer'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == '$*.*.CRONGO'
    assert lexer.token_list[2].type == TokenType.Variable
    assert lexer.token_list[3].text == ')'
    assert lexer.token_list[3].type == TokenType.Rp
    assert lexer.token_list[4].text == '&&'
    assert lexer.token_list[4].type == TokenType.And
    assert lexer.token_list[5].text == '$*.*.CRONGO'
    assert lexer.token_list[5].type == TokenType.Variable
    assert lexer.token_list[6].text == '=='
    assert lexer.token_list[6].type == TokenType.Eq
    assert lexer.token_list[7].text == '\'Y\''
    assert lexer.token_list[7].type == TokenType.Identifier
    assert lexer.token_list[8].text == '?'
    assert lexer.token_list[8].type == TokenType.Question
    assert lexer.token_list[9].text == '$*.*.*'
    assert lexer.token_list[9].type == TokenType.Variable
    assert lexer.token_list[10].text == '=='
    assert lexer.token_list[10].type == TokenType.Eq
    assert lexer.token_list[11].text == '\'\''
    assert lexer.token_list[11].type == TokenType.Identifier
    assert lexer.token_list[12].text == ':'
    assert lexer.token_list[12].type == TokenType.Colon
    assert lexer.token_list[13].text == 'true'
    assert lexer.token_list[13].type == TokenType.TRUE


    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer7(rules):
    string = StringIO(rules[7])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == 'mustAnswer'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == '$*.*.CRONGO'
    assert lexer.token_list[2].type == TokenType.Variable
    assert lexer.token_list[3].text == ')'
    assert lexer.token_list[3].type == TokenType.Rp
    assert lexer.token_list[4].text == '&&'
    assert lexer.token_list[4].type == TokenType.And
    assert lexer.token_list[5].text == '$*.*.CRONGO'
    assert lexer.token_list[5].type == TokenType.Variable
    assert lexer.token_list[6].text == '=='
    assert lexer.token_list[6].type == TokenType.Eq
    assert lexer.token_list[7].text == '\'N\''
    assert lexer.token_list[7].type == TokenType.Identifier
    assert lexer.token_list[8].text == '?'
    assert lexer.token_list[8].type == TokenType.Question
    assert lexer.token_list[9].text == '$*.*.*'
    assert lexer.token_list[9].type == TokenType.Variable
    assert lexer.token_list[10].text == '!='
    assert lexer.token_list[10].type == TokenType.NEq
    assert lexer.token_list[11].text == '\'\''
    assert lexer.token_list[11].type == TokenType.Identifier
    assert lexer.token_list[12].text == ':'
    assert lexer.token_list[12].type == TokenType.Colon
    assert lexer.token_list[13].text == 'true'
    assert lexer.token_list[13].type == TokenType.TRUE
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer8(rules):
    string = StringIO(rules[8])
    lexer = Lexer()
    lexer.tokenize(string)

    assert len(lexer.token_list) == 10
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer9(rules):
    string = StringIO(rules[4])
    lexer = Lexer()
    lexer.tokenize(string)

    assert len(lexer.token_list) == 3
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer10(rules):
    string = StringIO(rules[10])
    lexer = Lexer()
    lexer.tokenize(string)
    # dipsplay(string, lexer)
    assert len(lexer.token_list) == 48
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer11(rules):
    string = StringIO(rules[11])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == 'toDate'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == '$C1D1.ONC-392 Administration.ECSTDAT'
    assert lexer.token_list[2].type == TokenType.Variable
    assert lexer.token_list[3].text == ')'
    assert lexer.token_list[3].type == TokenType.Rp
    assert lexer.token_list[4].text == '!='
    assert lexer.token_list[4].type == TokenType.NEq
    assert lexer.token_list[5].text == '""'
    assert lexer.token_list[5].type == TokenType.Identifier
    assert lexer.token_list[6].text == '&&'
    assert lexer.token_list[6].type == TokenType.And
    assert lexer.token_list[7].text == ' '
    assert lexer.token_list[7].type == TokenType.Blank
    assert lexer.token_list[8].text == 'toDate'
    assert lexer.token_list[8].type == TokenType.Identifier
    assert lexer.token_list[9].text == '('
    assert lexer.token_list[9].type == TokenType.Lp
    assert lexer.token_list[10].text == '$*.*.LBDAT'
    assert lexer.token_list[10].type == TokenType.Variable
    assert lexer.token_list[11].text == ')'
    assert lexer.token_list[11].type == TokenType.Rp
    assert lexer.token_list[12].text == '!='
    assert lexer.token_list[12].type == TokenType.NEq
    assert lexer.token_list[13].text == '""'
    assert lexer.token_list[13].type == TokenType.Identifier
    assert lexer.token_list[14].text == '&&'
    assert lexer.token_list[14].type == TokenType.And
    assert lexer.token_list[15].text == ' '
    assert lexer.token_list[15].type == TokenType.Blank
    assert lexer.token_list[16].text == 'toDate'
    assert lexer.token_list[16].type == TokenType.Identifier
    assert lexer.token_list[17].text == '('
    assert lexer.token_list[17].type == TokenType.Lp
    assert lexer.token_list[18].text == '"2015-1-12 "'
    assert lexer.token_list[18].type == TokenType.Identifier
    assert lexer.token_list[19].text == '+'
    assert lexer.token_list[19].type == TokenType.Plus
    assert lexer.token_list[20].text == '$C1D1.ONC-392 Administration.ECSTTIM'
    assert lexer.token_list[20].type == TokenType.Variable
    assert lexer.token_list[21].text == '+'
    assert lexer.token_list[21].type == TokenType.Plus
    assert lexer.token_list[22].text == '":00"'
    assert lexer.token_list[22].type == TokenType.Identifier
    assert lexer.token_list[23].text == ')'
    assert lexer.token_list[23].type == TokenType.Rp
    assert lexer.token_list[24].text == '!='
    assert lexer.token_list[24].type == TokenType.NEq
    assert lexer.token_list[25].text == '""'
    assert lexer.token_list[25].type == TokenType.Identifier
    assert lexer.token_list[26].text == ' '
    assert lexer.token_list[26].type == TokenType.Blank
    assert lexer.token_list[27].text == '&&'
    assert lexer.token_list[27].type == TokenType.And
    assert lexer.token_list[28].text == 'toDate'
    assert lexer.token_list[28].type == TokenType.Identifier
    assert lexer.token_list[29].text == '('
    assert lexer.token_list[29].type == TokenType.Lp
    assert lexer.token_list[30].text == '"2015-1-12 "'
    assert lexer.token_list[30].type == TokenType.Identifier
    assert lexer.token_list[31].text == '+'
    assert lexer.token_list[31].type == TokenType.Plus
    assert lexer.token_list[32].text == '$*.*.*'
    assert lexer.token_list[32].type == TokenType.Variable
    assert lexer.token_list[33].text == '+'
    assert lexer.token_list[33].type == TokenType.Plus
    assert lexer.token_list[34].text == '":00"'
    assert lexer.token_list[34].type == TokenType.Identifier
    assert lexer.token_list[35].text == ')'
    assert lexer.token_list[35].type == TokenType.Rp
    assert lexer.token_list[36].text == '!='
    assert lexer.token_list[36].type == TokenType.NEq
    assert lexer.token_list[37].text == '""'
    assert lexer.token_list[37].type == TokenType.Identifier
    assert lexer.token_list[38].text == '?'
    assert lexer.token_list[38].type == TokenType.Question
    assert lexer.token_list[39].text == 'dateDiff'
    assert lexer.token_list[39].type == TokenType.Identifier
    assert lexer.token_list[40].text == '('
    assert lexer.token_list[40].type == TokenType.Lp
    assert lexer.token_list[41].text == '$C1D1.ONC-392 Administration.ECSTDAT'
    assert lexer.token_list[41].type == TokenType.Variable
    assert lexer.token_list[42].text == '+'
    assert lexer.token_list[42].type == TokenType.Plus
    assert lexer.token_list[43].text == '" "'
    assert lexer.token_list[43].type == TokenType.Identifier
    assert lexer.token_list[44].text == '+'
    assert lexer.token_list[44].type == TokenType.Plus
    assert lexer.token_list[45].text == '$C1D1.ONC-392 Administration.ECSTTIM'
    assert lexer.token_list[45].type == TokenType.Variable
    assert lexer.token_list[46].text == '+'
    assert lexer.token_list[46].type == TokenType.Plus
    assert lexer.token_list[47].text == '":00"'
    assert lexer.token_list[47].type == TokenType.Identifier
    assert lexer.token_list[48].text == ','
    assert lexer.token_list[48].type == TokenType.Comma
    assert lexer.token_list[49].text == '$*.*.LBDAT'
    assert lexer.token_list[49].type == TokenType.Variable
    assert lexer.token_list[50].text == '+'
    assert lexer.token_list[50].type == TokenType.Plus
    assert lexer.token_list[51].text == '" "'
    assert lexer.token_list[51].type == TokenType.Identifier
    assert lexer.token_list[52].text == '+'
    assert lexer.token_list[52].type == TokenType.Plus
    assert lexer.token_list[53].text == '$*.*.*'
    assert lexer.token_list[53].type == TokenType.Variable
    assert lexer.token_list[54].text == '+'
    assert lexer.token_list[54].type == TokenType.Plus
    assert lexer.token_list[55].text == '":00"'
    assert lexer.token_list[55].type == TokenType.Identifier
    assert lexer.token_list[56].text == ','
    assert lexer.token_list[56].type == TokenType.Comma
    assert lexer.token_list[57].text == '"m"'
    assert lexer.token_list[57].type == TokenType.Identifier
    assert lexer.token_list[58].text == ')'
    assert lexer.token_list[58].type == TokenType.Rp
    assert lexer.token_list[59].text == '>'
    assert lexer.token_list[59].type == TokenType.Gt
    assert lexer.token_list[60].text == '0'
    assert lexer.token_list[60].type == TokenType.RealNumber
    assert lexer.token_list[61].text == ':'
    assert lexer.token_list[61].type == TokenType.Colon
    assert lexer.token_list[62].text == 'true'
    assert lexer.token_list[62].type == TokenType.TRUE
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def test_rule_lexer12(rules):
    string = StringIO(rules[12])
    lexer = Lexer()
    lexer.tokenize(string)

    assert lexer.token_list[0].text == 'autoValue'
    assert lexer.token_list[0].type == TokenType.Identifier
    assert lexer.token_list[1].text == '('
    assert lexer.token_list[1].type == TokenType.Lp
    assert lexer.token_list[2].text == 'RoundN'
    assert lexer.token_list[2].type == TokenType.Identifier
    assert lexer.token_list[3].text == '('
    assert lexer.token_list[3].type == TokenType.Lp
    assert lexer.token_list[4].text == 'sum'
    assert lexer.token_list[4].type == TokenType.Identifier
    assert lexer.token_list[5].text == '('
    assert lexer.token_list[5].type == TokenType.Lp
    assert lexer.token_list[6].text == 'getSumOfItemInLog'
    assert lexer.token_list[6].type == TokenType.Identifier
    assert lexer.token_list[7].text == '('
    assert lexer.token_list[7].type == TokenType.Lp
    assert lexer.token_list[8].text == '$*.Target Lesions Assessment (Details) (Screening).TLLONG'
    assert lexer.token_list[8].type == TokenType.Variable
    assert lexer.token_list[9].text == ','
    assert lexer.token_list[9].type == TokenType.Comma
    assert lexer.token_list[10].text == ' '
    assert lexer.token_list[10].type == TokenType.Blank
    assert lexer.token_list[11].text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert lexer.token_list[11].type == TokenType.Variable
    assert lexer.token_list[12].text == '!='
    assert lexer.token_list[12].type == TokenType.NEq
    assert lexer.token_list[13].text == ' '
    assert lexer.token_list[13].type == TokenType.Blank
    assert lexer.token_list[14].text == '11'
    assert lexer.token_list[14].type == TokenType.RealNumber
    assert lexer.token_list[15].text == ' '
    assert lexer.token_list[15].type == TokenType.Blank
    assert lexer.token_list[16].text == '&&'
    assert lexer.token_list[16].type == TokenType.And
    assert lexer.token_list[17].text == ' '
    assert lexer.token_list[17].type == TokenType.Blank
    assert lexer.token_list[18].text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU '
    assert lexer.token_list[18].type == TokenType.Variable
    assert lexer.token_list[19].text == '=='
    assert lexer.token_list[19].type == TokenType.Eq
    assert lexer.token_list[20].text == ' '
    assert lexer.token_list[20].type == TokenType.Blank
    assert lexer.token_list[21].text == '"CM"'
    assert lexer.token_list[21].type == TokenType.Identifier
    assert lexer.token_list[22].text == ')'
    assert lexer.token_list[22].type == TokenType.Rp
    assert lexer.token_list[23].text == ' '
    assert lexer.token_list[23].type == TokenType.Blank
    assert lexer.token_list[24].text == ','
    assert lexer.token_list[24].type == TokenType.Comma
    assert lexer.token_list[25].text == ' '
    assert lexer.token_list[25].type == TokenType.Blank
    assert lexer.token_list[26].text == 'multiply'
    assert lexer.token_list[26].type == TokenType.Identifier
    assert lexer.token_list[27].text == '('
    assert lexer.token_list[27].type == TokenType.Lp
    assert lexer.token_list[28].text == 'getSumOfItemInLog'
    assert lexer.token_list[28].type == TokenType.Identifier
    assert lexer.token_list[29].text == '('
    assert lexer.token_list[29].type == TokenType.Lp
    assert lexer.token_list[30].text == '$*.Target Lesions Assessment (Details) (Screening).TLLONG'
    assert lexer.token_list[30].type == TokenType.Variable
    assert lexer.token_list[31].text == ','
    assert lexer.token_list[31].type == TokenType.Comma
    assert lexer.token_list[32].text == ' '
    assert lexer.token_list[32].type == TokenType.Blank
    assert lexer.token_list[33].text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert lexer.token_list[33].type == TokenType.Variable
    assert lexer.token_list[34].text == '!='
    assert lexer.token_list[34].type == TokenType.NEq
    assert lexer.token_list[35].text == ' '
    assert lexer.token_list[35].type == TokenType.Blank
    assert lexer.token_list[36].text == '11'
    assert lexer.token_list[36].type == TokenType.RealNumber
    assert lexer.token_list[37].text == ' '
    assert lexer.token_list[37].type == TokenType.Blank
    assert lexer.token_list[38].text == '&&'
    assert lexer.token_list[38].type == TokenType.And
    assert lexer.token_list[39].text == ' '
    assert lexer.token_list[39].type == TokenType.Blank
    assert lexer.token_list[40].text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU '
    assert lexer.token_list[40].type == TokenType.Variable
    assert lexer.token_list[41].text == '=='
    assert lexer.token_list[41].type == TokenType.Eq
    assert lexer.token_list[42].text == ' '
    assert lexer.token_list[42].type == TokenType.Blank
    assert lexer.token_list[43].text == '"MM"'
    assert lexer.token_list[43].type == TokenType.Identifier
    assert lexer.token_list[44].text == ')'
    assert lexer.token_list[44].type == TokenType.Rp
    assert lexer.token_list[45].text == ','
    assert lexer.token_list[45].type == TokenType.Comma
    assert lexer.token_list[46].text == '1'
    assert lexer.token_list[46].type == TokenType.RealNumber
    assert lexer.token_list[47].text == '/'
    assert lexer.token_list[47].type == TokenType.Divide
    assert lexer.token_list[48].text == '10'
    assert lexer.token_list[48].type == TokenType.RealNumber
    assert lexer.token_list[49].text == ')'
    assert lexer.token_list[49].type == TokenType.Rp
    assert lexer.token_list[50].text == ' '
    assert lexer.token_list[50].type == TokenType.Blank
    assert lexer.token_list[51].text == ','
    assert lexer.token_list[51].type == TokenType.Comma
    assert lexer.token_list[52].text == ' '
    assert lexer.token_list[52].type == TokenType.Blank
    assert lexer.token_list[53].text == 'getSumOfItemInLog'
    assert lexer.token_list[53].type == TokenType.Identifier
    assert lexer.token_list[54].text == '('
    assert lexer.token_list[54].type == TokenType.Lp
    assert lexer.token_list[55].text == '$*.Target Lesions Assessment (Details) (Screening).TLSHORT'
    assert lexer.token_list[55].type == TokenType.Variable
    assert lexer.token_list[56].text == ','
    assert lexer.token_list[56].type == TokenType.Comma
    assert lexer.token_list[57].text == ' '
    assert lexer.token_list[57].type == TokenType.Blank
    assert lexer.token_list[58].text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert lexer.token_list[58].type == TokenType.Variable
    assert lexer.token_list[59].text == '=='
    assert lexer.token_list[59].type == TokenType.Eq
    assert lexer.token_list[60].text == ' '
    assert lexer.token_list[60].type == TokenType.Blank
    assert lexer.token_list[61].text == '11'
    assert lexer.token_list[61].type == TokenType.RealNumber
    assert lexer.token_list[62].text == ' '
    assert lexer.token_list[62].type == TokenType.Blank
    assert lexer.token_list[63].text == '&&'
    assert lexer.token_list[63].type == TokenType.And
    assert lexer.token_list[64].text == ' '
    assert lexer.token_list[64].type == TokenType.Blank
    assert lexer.token_list[65].text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU'
    assert lexer.token_list[65].type == TokenType.Variable
    assert lexer.token_list[66].text == '=='
    assert lexer.token_list[66].type == TokenType.Eq
    assert lexer.token_list[67].text == ' '
    assert lexer.token_list[67].type == TokenType.Blank
    assert lexer.token_list[68].text == '"CM"'
    assert lexer.token_list[68].type == TokenType.Identifier
    assert lexer.token_list[69].text == ')'
    assert lexer.token_list[69].type == TokenType.Rp
    assert lexer.token_list[70].text == ' '
    assert lexer.token_list[70].type == TokenType.Blank
    assert lexer.token_list[71].text == ','
    assert lexer.token_list[71].type == TokenType.Comma
    assert lexer.token_list[72].text == ' '
    assert lexer.token_list[72].type == TokenType.Blank
    assert lexer.token_list[73].text == 'multiply'
    assert lexer.token_list[73].type == TokenType.Identifier
    assert lexer.token_list[74].text == '('
    assert lexer.token_list[74].type == TokenType.Lp
    assert lexer.token_list[75].text == 'getSumOfItemInLog'
    assert lexer.token_list[75].type == TokenType.Identifier
    assert lexer.token_list[76].text == '('
    assert lexer.token_list[76].type == TokenType.Lp
    assert lexer.token_list[77].text == '$*.Target Lesions Assessment (Details) (Screening).TLSHORT'
    assert lexer.token_list[77].type == TokenType.Variable
    assert lexer.token_list[78].text == ','
    assert lexer.token_list[78].type == TokenType.Comma
    assert lexer.token_list[79].text == ' '
    assert lexer.token_list[79].type == TokenType.Blank
    assert lexer.token_list[80].text == '$*.Target Lesions Assessment (Details) (Screening).TLLOC '
    assert lexer.token_list[80].type == TokenType.Variable
    assert lexer.token_list[81].text == '=='
    assert lexer.token_list[81].type == TokenType.Eq
    assert lexer.token_list[82].text == ' '
    assert lexer.token_list[82].type == TokenType.Blank
    assert lexer.token_list[83].text == '11'
    assert lexer.token_list[83].type == TokenType.RealNumber
    assert lexer.token_list[84].text == ' '
    assert lexer.token_list[84].type == TokenType.Blank
    assert lexer.token_list[85].text == '&&'
    assert lexer.token_list[85].type == TokenType.And
    assert lexer.token_list[86].text == ' '
    assert lexer.token_list[86].type == TokenType.Blank
    assert lexer.token_list[87].text == '$*.Target Lesions Assessment (Details) (Screening).TLDIAU'
    assert lexer.token_list[87].type == TokenType.Variable
    assert lexer.token_list[88].text == '=='
    assert lexer.token_list[88].type == TokenType.Eq
    assert lexer.token_list[89].text == ' '
    assert lexer.token_list[89].type == TokenType.Blank
    assert lexer.token_list[90].text == '"MM"'
    assert lexer.token_list[90].type == TokenType.Identifier
    assert lexer.token_list[91].text == ')'
    assert lexer.token_list[91].type == TokenType.Rp
    assert lexer.token_list[92].text == ','
    assert lexer.token_list[92].type == TokenType.Comma
    assert lexer.token_list[93].text == '1'
    assert lexer.token_list[93].type == TokenType.RealNumber
    assert lexer.token_list[94].text == '/'
    assert lexer.token_list[94].type == TokenType.Divide
    assert lexer.token_list[95].text == '10'
    assert lexer.token_list[95].type == TokenType.RealNumber
    assert lexer.token_list[96].text == ')'
    assert lexer.token_list[96].type == TokenType.Rp
    assert lexer.token_list[97].text == ')'
    assert lexer.token_list[97].type == TokenType.Rp
    assert lexer.token_list[98].text == ','
    assert lexer.token_list[98].type == TokenType.Comma
    assert lexer.token_list[99].text == ' '
    assert lexer.token_list[99].type == TokenType.Blank
    assert lexer.token_list[100].text == '0.01'
    assert lexer.token_list[100].type == TokenType.RealNumber
    assert lexer.token_list[101].text == ')'
    assert lexer.token_list[101].type == TokenType.Rp
    assert lexer.token_list[102].text == ','
    assert lexer.token_list[102].type == TokenType.Comma
    assert lexer.token_list[103].text == ' '
    assert lexer.token_list[103].type == TokenType.Blank
    assert lexer.token_list[104].text == 'true'
    assert lexer.token_list[104].type == TokenType.TRUE
    assert lexer.token_list[105].text == ')'
    assert lexer.token_list[105].type == TokenType.Rp
    r = "".join([token.text for token in lexer.token_list])
    assert r == string.getvalue()


def display(lexer):
    for i, t in enumerate(lexer.token_list):
        print("assert", f'lexer.token_list[{i}].text == \'{t.text}\'')
        print("assert", f'lexer.token_list[{i}].type == {t.type}')
