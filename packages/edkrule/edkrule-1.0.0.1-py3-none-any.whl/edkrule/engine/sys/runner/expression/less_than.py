from edkrule.engine.runner import Runner


class LessThan(Runner):
    def execute(self, *args):
        return args[0] <= args[1]
