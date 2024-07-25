from edkrule.engine.runner import Runner


class AutoIncrease(Runner):
    def execute(self, *args):
        return sum(args)
