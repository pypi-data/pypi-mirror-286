

from edkrule.interpreter.ops.abstract_op import AbstractOp


class BaseOP(AbstractOp):
    def action(self): ...
