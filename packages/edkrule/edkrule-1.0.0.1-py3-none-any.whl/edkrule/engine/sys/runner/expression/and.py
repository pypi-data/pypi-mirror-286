from edkrule.engine.runner import Runner


class And(Runner):
    def execute(self, *args):
        return args[0] and args[1]