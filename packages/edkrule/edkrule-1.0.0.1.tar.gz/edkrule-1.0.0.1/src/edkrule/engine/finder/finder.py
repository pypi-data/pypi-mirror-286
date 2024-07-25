import abc


class Finder(abc.ABC):
    @abc.abstractmethod
    def find(self, expression, find_parameter): ...
