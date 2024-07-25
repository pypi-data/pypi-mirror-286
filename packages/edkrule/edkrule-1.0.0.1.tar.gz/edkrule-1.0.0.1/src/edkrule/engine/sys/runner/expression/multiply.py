from edkrule.engine.runner import Runner


class Multiply(Runner):
    def execute(self, *args):
        return args[0] * args[1]