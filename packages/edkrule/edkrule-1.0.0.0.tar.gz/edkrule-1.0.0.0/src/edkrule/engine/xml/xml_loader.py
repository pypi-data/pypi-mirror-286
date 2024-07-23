from lxml import etree

from edkrule.engine.constant import Constant




class XMLLoader:
    def __init__(self, path):
        self.xml_define = etree.parse(path)

    @property
    def namespace(self):
        return "{http://www.edkrule.org/XMLSchema}"

    def equal(self, tag: str, element_name: str) -> bool:
        return tag.replace(self.namespace, "").lower() == element_name

    def text(self, tag) -> str:
        return tag.replace(self.namespace, "").lower()

    def loader(self, engine_definition):
        root = self.xml_define.getroot()

        if root.attrib.get("parent") is not None:
            XMLLoader(root.attrib.get("parent")).loader(engine_definition)

        for e in self.xml_define.getroot():
            if self.equal(e.tag, Constant.DataTypes):
                self.data_type_definition(e, engine_definition)
            elif self.equal(e.tag, Constant.Expressions):
                self.expression_definition(e, engine_definition)
            elif self.equal(e.tag, Constant.Identifiers):
                self.identifier_definition(e, engine_definition)

    def class_info_load(self, engine_definition_type, element, engine_definition):
        package = element.attrib.get(Constant.Package)
        for e in element:
            engine_definition.set(engine_definition_type, e.attrib.get(Constant.Name).lower(), {
                Constant.Package: e.attrib.get(Constant.Package) or package,
                Constant.Class: e.attrib.get(Constant.Class)})

    def data_type_definition(self, element, engine_definition):
        self.class_info_load(Constant.DataTypes, element, engine_definition)

    def expression_definition(self, element, engine_definition):
        self.class_info_load(Constant.Expressions, element, engine_definition)

    def identifier_definition(self, element, engine_definition):
        self.class_info_load(Constant.Identifiers, element, engine_definition)

