import abc
# from pybiz.tests.interpreter.parse.parser import Parser


class AbcStatementParser(abc.ABC):

    def __init__(self, parser):
        self.parser = parser

    @abc.abstractmethod
    def accept(self) -> bool: ...

    def token(self, offset: int = 0):
        return self.parser.body[self.parser.index + offset]

    def move(self, pos: int = 1):
        self.parser.index += pos
