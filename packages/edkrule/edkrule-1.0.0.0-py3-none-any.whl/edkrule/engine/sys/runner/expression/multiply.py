from edkrule.engine.runner import Runner


class Multiply(Runner):
    def run(self, *args):
        return args[0] * args[1]