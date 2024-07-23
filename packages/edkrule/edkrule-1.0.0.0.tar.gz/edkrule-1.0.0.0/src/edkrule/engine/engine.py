from edkrule.engine.engine_definition import EngineDefinition
from edkrule.engine.sys.sys_path import sys_path
from edkrule.engine.xml.xml_loader import XMLLoader


class Engine:
    def __init__(self, definition_path, use_sys=True):
        self._definition_path = definition_path
        self._engine_definition = EngineDefinition()
        self.re_loader(definition_path=self._definition_path, use_sys=use_sys)

    def re_loader(self, definition_path, use_sys=True, clear=True):
        if clear: self._engine_definition = EngineDefinition()
        if use_sys: XMLLoader(sys_path()).loader(engine_definition=self._engine_definition)
        XMLLoader(definition_path).loader(engine_definition=self._engine_definition)

    def get(self, definition_type, name: str):
        return self._engine_definition.get(definition_type, name.lower())

    def get_class(self, definition_type, name: str):
        return self._engine_definition.get_class(definition_type, name.lower())

    @property
    def definition(self): return self._engine_definition

    # def get(self, key):
    #     return self._engine_definition.get(key)
