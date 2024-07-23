from edkrule.engine.runner import Runner


class RealNumber(Runner):
    def run(self, *args):
        return int(args[0])
