from edkrule.engine.runner import Runner


class Variable(Runner):
    def execute(self, *args):
        return args[0]