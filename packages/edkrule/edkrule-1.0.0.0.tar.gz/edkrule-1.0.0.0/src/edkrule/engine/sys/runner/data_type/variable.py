from edkrule.engine.runner import Runner


class Variable(Runner):
    def run(self, *args):
        return args[0]