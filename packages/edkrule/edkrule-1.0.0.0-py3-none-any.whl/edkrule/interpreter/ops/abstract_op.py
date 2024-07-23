import abc
import uuid

from edkrule.constants.Identifier import Identifier
from edkrule.constants.op_type import OPType


class AbstractOp(abc.ABC):
    def __init__(self, name, ot: OPType = OPType.Get, *arguments):
        self._next = None
        self._prev = None
        self._name = name
        self._id = str(uuid.uuid4())
        self._arguments = arguments
        self._result = Identifier.Void
        self._interpreter = None

    @property
    def id(self): return self._id

    @property
    def interpreter(self): return self._interpreter

    @interpreter.setter
    def interpreter(self, value): self._interpreter = value

    @property
    def arguments(self): return self._arguments

    def set_arguments(self, *arguments):
        self._arguments = arguments

    @property
    def next(self): return self._next

    @property
    def name(self): return self._name

    @next.setter
    def next(self, next_op):
        self._next = next_op
        next_op._prev = self

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, prev_op):
        self._prev = prev_op
        prev_op._next = self

    @abc.abstractmethod
    def action(self): ...

    def ret(self):
        self.action()
        return {self.id: {"#name": self._name, "#ret": self._result}}
