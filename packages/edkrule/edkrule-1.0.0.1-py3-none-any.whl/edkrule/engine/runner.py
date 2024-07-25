import abc

from edkrule.utils.cache import Cache
from edkrule.utils.squeue import Squeue


class Runner(abc.ABC):
    def __init__(self, engine, rid):
        self._engine = engine
        self.rid = rid

    def run(self, *args):
        """
        step1. 计算结果
        step2. 计算结果存储在 cache 中
        :param args:
        :type args:
        :return:
        :rtype:
        """
        result = self.execute(*args)
        self.cache().set(self.rid, result)
        self.squeue().append(self.rid)
        return result

    @abc.abstractmethod
    def execute(self, *args): ...

    def cache(self) -> Cache:
        return self._engine.cache

    def squeue(self) -> Squeue:
        return self._engine.squeue
