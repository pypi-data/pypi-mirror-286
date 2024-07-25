from edkrule.utils.cache import Cache
from edkrule.engine.engine_definition import EngineDefinition
from edkrule.engine.sys.sys_path import sys_path
from edkrule.engine.xml.xml_loader import XMLLoader
from edkrule.utils.squeue import Squeue


class Engine:
    def __init__(self, definition_path, use_sys=True):
        self._cache = Cache()
        self._squeue = Squeue()
        self._definition_path = definition_path
        self._engine_definition = EngineDefinition()
        self.re_loader(definition_path=self._definition_path, use_sys=use_sys)

    @property
    def cache(self): return self._cache

    @property
    def squeue(self): return self._squeue

    def re_loader(self, definition_path, use_sys=True, clear=True):
        """
        传参方式 1.
            definition_path = “” and use_sys=True 只是用系统默认规则引擎
        传参方式 2.
            definition_path = “xxxxx” and use_sys=True 同时加载传入的引擎配置和系统默认规则引擎
            如果有相同的名字的，加载传入的引擎配置会覆盖系统默认的配置
        传参方式 3.
            definition_path = “xxxxx” and use_sys=False 只加载传入的引擎配置
        加载 引擎的 XML 配置
        :param definition_path: 加载的 引擎配置的 XML 路径
        :type definition_path:
        :param use_sys: 是否加载系统默认的规则
        :type use_sys:
        :param clear: 重新加载的时候，是否清楚原配置
        :type clear:
        :return:
        :rtype:
        """
        if clear: self._engine_definition = EngineDefinition()
        if use_sys: XMLLoader(sys_path()).loader(engine_definition=self._engine_definition)
        if len(definition_path) != 0:
            XMLLoader(definition_path).loader(engine_definition=self._engine_definition)

    def get(self, definition_type, name: str):
        return self._engine_definition.get(definition_type, name.lower())

    def get_class(self, definition_type, name: str):
        return self._engine_definition.get_class(definition_type, name.lower())

    @property
    def definition(self):
        return self._engine_definition

    # def get(self, key):
    #     return self._engine_definition.get(key)
