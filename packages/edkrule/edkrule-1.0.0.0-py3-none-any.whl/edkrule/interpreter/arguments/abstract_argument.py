import abc


class AbstractArgument(abc.ABC):
    def __init__(self, body):
        self._body = body

    @property
    def body(self): return self._body

    @abc.abstractmethod
    def get(self): ...
