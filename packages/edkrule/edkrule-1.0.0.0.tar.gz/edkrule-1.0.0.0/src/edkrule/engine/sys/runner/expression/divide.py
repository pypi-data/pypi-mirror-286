from edkrule.engine.runner import Runner


class Divide(Runner):
    def run(self, *args):
        return args[0] / args[1]
