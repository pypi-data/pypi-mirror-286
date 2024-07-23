from edkrule.interpreter.arguments.abstract_argument import AbstractArgument


class ValueArgument(AbstractArgument):
    def __init__(self, body):
        super().__init__(body)

    def get(self):
        return self.body
