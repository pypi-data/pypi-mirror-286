from typing import Optional

from edkrule.interpreter.linear.linear import Linear
from edkrule.interpreter.linear.op_stack import OpStack


class ExeQueue(Linear):
    def __init__(self):
        super().__init__()

    def append(self, ops: OpStack):
        self._list.append(ops)

    def head(self) -> Optional[OpStack]:
        if self.length() > 0:
            self._point.increment()
            self._length.decrement()
            return self._list[self._point.get()]
        return None

    def reset(self):
        super(ExeQueue,  self).reset()
        map(lambda op: op.reset(), self._list)

