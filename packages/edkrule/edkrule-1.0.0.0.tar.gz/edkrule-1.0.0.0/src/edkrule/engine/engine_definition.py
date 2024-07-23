import importlib

from edkrule.engine.constant import Constant


class EngineDefinition:
    def __init__(self):
        self._definition = {
            Constant.DataTypes: {},
            Constant.Identifiers: {},
            Constant.Expressions: {}
        }

    def set(self, engine_definition_type, key, value):
        self._definition[engine_definition_type][key] = value

    def get(self, engine_definition_type, name):
        return self._definition[engine_definition_type].get(name)

    def get_class(self, engine_definition_type, name):
        class_info = None
        if engine_definition_type == Constant.DataTypes:
            class_info = self.data_type(name)
        elif engine_definition_type == Constant.Expressions:
            class_info = self.expression(name)
        elif engine_definition_type == Constant.Identifiers:
            class_info = self.identifier(name)
        if class_info is None: return None
        return self.class_loader(class_info)

    def class_loader(self, class_info):
        pkg, clazz_name = class_info.get(Constant.Package), class_info.get(Constant.Class).split(".")
        module = importlib.import_module(pkg+f".{clazz_name[0]}")
        entry_clazz = getattr(module, clazz_name[1])
        return entry_clazz

    def data_type(self, name):
        return self._definition[Constant.DataTypes].get(name)

    def identifier(self, name):
        class_info = self._definition[Constant.Identifiers].get(name)
        if class_info is None:
            class_info = self._definition[Constant.Identifiers].get(Constant.DefaultIdentifier)
        return class_info

    def expression(self, name):
        return self._definition[Constant.Expressions].get(name)
