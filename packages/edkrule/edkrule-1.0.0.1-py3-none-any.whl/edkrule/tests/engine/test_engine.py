from io import StringIO

from edkrule.edk_rule import EdkRule
from edkrule.engine.constant import Constant
from edkrule.engine.engine import Engine
from edkrule.engine.finder.by import By
from edkrule.interpreter.expression.interpreter import Interpreter
from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.parse.parser import Parser


def case0():
    engine = Engine(
        definition_path="D:\\aws\\eclinical40_auto_testing\\edkrule\\src\\edkrule\\tests\\engine\\engine.xml")
    assert engine.get(Constant.DataTypes, 'realNumber').get(Constant.Package) == 'dp1'
    assert engine.get(Constant.DataTypes, 'realNumber').get(Constant.Class) == 'dc1'
    assert engine.get(Constant.DataTypes, 'VarIable').get(Constant.Package) == 'dp2'
    assert engine.get(Constant.DataTypes, 'VarIable').get(Constant.Class) == 'dc2'
    assert engine.get(Constant.Identifiers, 'xx').get(Constant.Package) == 'sp1'
    assert engine.get(Constant.Identifiers, 'xx').get(Constant.Class) == 'sc1'
    assert engine.get(Constant.Identifiers, 'yyy').get(Constant.Package) == 'sp2'
    assert engine.get(Constant.Identifiers, 'YYy').get(Constant.Class) == 'sc2'
    assert engine.get(Constant.Expressions, '+').get(Constant.Package) == 'ep1'
    assert engine.get(Constant.Expressions, '+').get(Constant.Class) == 'ec1'
    assert engine.get(Constant.Expressions, '-').get(Constant.Package) == 'ep2'
    assert engine.get(Constant.Expressions, '-').get(Constant.Class) == 'ec2'
    assert engine.get(Constant.Expressions, '||').get(Constant.Package) == 'ep'
    assert engine.get(Constant.Expressions, '||').get(Constant.Class) == 'ec3'
    assert engine.get(Constant.Expressions, '&&').get(Constant.Package) == 'ep'
    assert engine.get(Constant.Expressions, '&&').get(Constant.Class) == 'ec4'

    assert engine.definition.identifier("dasdsa").get(Constant.Package) == 'sp'
    assert engine.definition.identifier("dasdsa").get(Constant.Class) == 'ic'


def case1():
    engine = Engine(
        definition_path="D:\\aws\\eclinical40_auto_testing\\edkrule\\src\\edkrule\\tests\\engine\\engine0.xml")
    assert engine.get(Constant.DataTypes, 'realNumber').get(Constant.Package) == 'cdp1'
    assert engine.get(Constant.DataTypes, 'realNumber').get(Constant.Class) == 'cdc1'
    assert engine.get(Constant.DataTypes, 'VarIable').get(Constant.Package) == 'dp2'
    assert engine.get(Constant.DataTypes, 'VarIable').get(Constant.Class) == 'dc2'
    assert engine.get(Constant.Identifiers, 'xx').get(Constant.Package) == 'csp1'
    assert engine.get(Constant.Identifiers, 'xx').get(Constant.Class) == 'sc1'
    assert engine.get(Constant.Identifiers, 'yyy').get(Constant.Package) == 'sp2'
    assert engine.get(Constant.Identifiers, 'YYy').get(Constant.Class) == 'sc2'
    assert engine.get(Constant.Expressions, '+').get(Constant.Package) == 'ep1'
    assert engine.get(Constant.Expressions, '+').get(Constant.Class) == 'ec1'
    assert engine.get(Constant.Expressions, '-').get(Constant.Package) == 'ep2'
    assert engine.get(Constant.Expressions, '-').get(Constant.Class) == 'ec2'
    assert engine.get(Constant.Expressions, '||').get(Constant.Package) == 'cep3'
    assert engine.get(Constant.Expressions, '||').get(Constant.Class) == 'ec3'
    assert engine.get(Constant.Expressions, '&&').get(Constant.Package) == 'ep'
    assert engine.get(Constant.Expressions, '&&').get(Constant.Class) == 'ec4'
    assert engine.definition.identifier("dasdsa").get(Constant.Package) == 'sp'
    assert engine.definition.identifier("dasdsa").get(Constant.Class) == 'ic'


def evals(stringio):
    l = Lexer()
    l.tokenize(stringio)
    es = Parser(l.token_list)
    es.parse()
    exp = Interpreter().interpret(es.statement)
    return exp


def load_engine():
    engine = Engine(
        definition_path="D:\\aws\\eclinical40_auto_testing\\edkrule\\src\\edkrule\\tests\\engine\\engine2.xml")
    return engine


def case2():
    engine = load_engine()
    rule = StringIO("111")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 111
    rule = StringIO("a111")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == "a111"
    rule = StringIO("true")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True
    rule = StringIO("false")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == False


def case3():
    engine = load_engine()
    rule = StringIO("1+1+3")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 5


def case4():
    engine = load_engine()
    rule = StringIO("1==1?2:3")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 2
    engine = load_engine()
    rule = StringIO("1==2?2+1:3+5")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 8


def case5():
    engine = load_engine()
    rule = StringIO("1==2?2+1:3==4?4:5")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 5


def case6():
    engine = load_engine()
    rule = StringIO("toDate()?2+1:3==4?4:5")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 5


def case7():
    engine = load_engine()
    rule = StringIO("autoincrease(1,2,3,4)")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 10
    engine = load_engine()
    rule = StringIO("autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1)")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 14


def case8():
    engine = load_engine()
    rule = StringIO("$*.*.*")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == "$*.*.*"


def case9():
    engine = load_engine()
    rule = StringIO(
        "autoincrease(1,1)==2?autoincrease(1,1):autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1)")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 2
    engine = load_engine()
    rule = StringIO(
        "autoincrease(1,1)==3?autoincrease(1,1):autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1)")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 14


def case10():
    engine = load_engine()
    rule = StringIO(
        "autoincrease(autoincrease(1,1)==2?autoincrease(1,1):autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1),autoincrease(1,1)==3?autoincrease(1,1):autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1))")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 16


def case11():
    engine = load_engine()
    rule = StringIO("2!=1")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True
    engine = load_engine()
    rule = StringIO("2>=1")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True
    engine = load_engine()
    rule = StringIO("2>=2")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True
    engine = load_engine()
    rule = StringIO("1<=2")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True
    engine = load_engine()
    rule = StringIO("1<=1")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True


def case12():
    engine = load_engine()
    rule = StringIO("true && false")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == False
    engine = load_engine()
    rule = StringIO("true || false")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == True


def case13():
    engine = load_engine()
    rule = StringIO("1-2")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == -1
    engine = load_engine()
    rule = StringIO("1*2")
    exp = evals(rule)
    exp.engine = engine
    r = exp.run()
    assert r == 2
    r = EdkRule.run(rule_string="1/2")
    assert r.get() == 0.5


def case14():
    engine = load_engine()
    rule = StringIO("1-2")
    exp = evals(rule)
    exp.engine = engine
    exp.run()
    rid = exp.find(By.RuleFragment, "1").rid
    assert engine.cache.get(rid) == 1


def case15():
    # r = EdkRule.run(rule_string="1/2")
    # print(r.track())
    r = EdkRule.run(rule_string="autoincrease(autoincrease(1,1)==2?autoincrease(1,1):autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1),autoincrease(1,1)==3?autoincrease(1,1):autoincrease(autoincrease(1,1),autoincrease(autoincrease(1,1),1),3+1,4+1))")
    # r = EdkRule.run(rule_string="autoincrease(1,2)")
    print(r.track())

def test_debug():
    rule = StringIO("""condition(mustAnswer(toNum($*.*.*)), isRange($*.*.*, 40,160))""")
    exp = evals(rule)
    print(exp.text)
    rid = exp.find(By.RuleFragment, rule.getvalue()).rid
    assert rid != None

def test_cases():
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
