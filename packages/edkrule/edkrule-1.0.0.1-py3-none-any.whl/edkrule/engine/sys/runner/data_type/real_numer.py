from edkrule.engine.runner import Runner


class RealNumber(Runner):
    def execute(self, *args):
        return int(args[0])
