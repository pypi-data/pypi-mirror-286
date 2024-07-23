from edkrule.interpreter.arguments.ref_argument import RefArgument
from edkrule.interpreter.arguments.value_argument import ValueArgument
from edkrule.interpreter.linear.exe_queue import ExeQueue
from edkrule.interpreter.memory import Memory
from edkrule.interpreter.linear.op_stack import OpStack
from edkrule.interpreter.ops.abstract_op import AbstractOp


class Interpreter:
    def __init__(self):
        self._exe_queue = ExeQueue()
        self.memory = Memory()

    def add(self, ops: OpStack):
        self._exe_queue.append(ops)

    def run(self):
        self._exe_queue.reset()
        ops = self._exe_queue.head()
        while ops is not None:
            op = ops.pop()
            while op is not None:
                self.memory.add(op.ret())
                op = ops.pop()
            ops = self._exe_queue.head()

    def ast(self):
        edge = []
        nodes = []
        self._exe_queue.reset()
        ops = self._exe_queue.head()
        while ops is not None:
            sub_node = []
            sub_edge = []
            op = ops.end()
            self.display(op, sub_node, sub_edge)
            ops = self._exe_queue.head()
            nodes.append(sub_node)
            edge.append(sub_edge)
        return nodes, edge

    def display(self, op: AbstractOp, nodes=None, edge=None):
        if edge is None:
            edge = []
        if nodes is None:
            nodes = []
        nodes.append(dict(id=op.id, name=op.name))
        for argument in op.arguments:
            if type(argument) == ValueArgument:
                edge.append(dict(source=op.id, target=argument.body))
            elif type(argument) == RefArgument:
                edge.append(dict(source=op.id, target=argument.body.id))
                self.display(argument.body, nodes , edge)


