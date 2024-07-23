import abc


class Runner(abc.ABC):
    @abc.abstractmethod
    def run(self, *args): ...