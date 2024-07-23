from typing import Optional


from edkrule.constants.stack_pos import StackPos
from edkrule.interpreter.linear.linear import Linear
from edkrule.interpreter.ops.abstract_op import AbstractOp


class OpStack(Linear):
    def __init__(self):
        super().__init__()
        self._interpreter = None

    def push(self, op: AbstractOp, pos: StackPos = StackPos.End):
        if pos != StackPos.End and pos != StackPos.Top:
            raise Exception(f"UnExpect StackPos {pos}")

        """
        StackPos.End - 列表尾部添加元素
        StackPos.Top - 列表顶部添加元素
        """
        self._list.append(op) if pos == StackPos.End else self._list.insert(0, op)

        op.interpreter = self._interpreter
        self._point.increment()
        self._length.increment()

    def pop(self) -> Optional[AbstractOp]:
        if self.length() > 0:
            op = self._list[self._point.get()]
            self._point.decrement()
            self._length.decrement()
            return op
        return None

    def end(self) -> Optional[AbstractOp]:
        if self.length() > 0:
            op = self._list[0]
            return op
        raise Exception("empty stack")

    @property
    def interpreter(self): return self._interpreter

    @interpreter.setter
    def interpreter(self, value):
        self._interpreter = value
        for op in self._list:
            op.interpreter = self._interpreter



    @classmethod
    def factory(cls, op: AbstractOp, pos: StackPos = StackPos.End):
        """
        创建操作的调用栈,
        根操作如果作为栈顶元素, 表示该操作第一个执行
        根操作如果作为栈尾元素, 表示该操作最后一个执行
        :param op: 根操作
        :type op:
        :param pos: 根操作是作为栈顶元素还是栈尾元素
        :type pos:
        :return:
        :rtype:
        """
        ops = OpStack()
        i_op = op
        while i_op is not None:
            ops.push(i_op, pos)
            i_op = i_op.prev if pos == StackPos.End else i_op.next
        return ops
