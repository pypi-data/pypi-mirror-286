from io import StringIO

from edkrule.engine.engine import Engine
from edkrule.engine.result import Result
from edkrule.interpreter.expression.interpreter import Interpreter
from edkrule.interpreter.lexer.lexer import Lexer
from edkrule.interpreter.parse.parser import Parser


class EdkRule:
    @staticmethod
    def lexer(rule_string: str):
        """
        返回规则词法分析的结果
        :param rule_string:
        :type rule_string:
        :return:
        :rtype:
        """
        l = Lexer()
        l.tokenize(StringIO(rule_string))
        return l.token_list

    @staticmethod
    def parser(rule_string: str):
        """
        返回规则语法分析的结果
        :param rule_string:
        :type rule_string:
        :return:
        :rtype:
        """
        es = Parser(EdkRule.lexer(rule_string))
        es.parse()
        return es.statement

    @staticmethod
    def expression(rule_string: str):
        """
        返回规则表达式分析的结果
        :param rule_string:
        :type rule_string:
        :return:
        :rtype:
        """
        exp = Interpreter().interpret(EdkRule.parser(rule_string))
        return exp

    @staticmethod
    def run(rule_string: str, engine_path: str = "", use_sys=True) -> Result:
        """
        运行规则
        传参方式 1.
            engine_path = “” and use_sys=True 只是用系统默认规则引擎
        传参方式 2.
            engine_path = “xxxxx” and use_sys=True 同时加载传入的引擎配置和系统默认规则引擎
            如果有相同的名字的，加载传入的引擎配置会覆盖系统默认的配置
        传参方式 3.
            engine_path = “xxxxx” and use_sys=False 只加载传入的引擎配置
        :param rule_string: 规则字符串
        :type rule_string:
        :param engine_path: 加载的 引擎配置的 XML 路径
        :type engine_path:
        :param use_sys: 是否加载系统默认的规则
        :type use_sys:
        :return:
        :rtype:
        """
        engine = Engine(definition_path=engine_path, use_sys=use_sys)
        rule = EdkRule.expression(rule_string)
        rule.engine = engine
        rule.run()
        return Result(rule)
