from edkrule.engine.runner import Runner


class AutoIncrease(Runner):
    def run(self, *args):
        return sum(args)
