from edkrule.engine.runner import Runner


class And(Runner):
    def run(self, *args):
        return args[0] and args[1]