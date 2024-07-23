from edkrule.interpreter.arguments.abstract_argument import AbstractArgument
from edkrule.interpreter.ops.abstract_op import AbstractOp


class RefArgument(AbstractArgument):
    def __init__(self, body: AbstractOp):
        super().__init__(body)

    def get(self):
        return self.body.interpreter.memory.get(self.body.id)
