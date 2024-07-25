import abc


class Formater(abc.ABC):
    @abc.abstractmethod
    def initialize(self, string) -> str: ...