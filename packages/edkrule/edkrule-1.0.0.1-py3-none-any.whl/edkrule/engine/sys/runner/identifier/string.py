from edkrule.engine.runner import Runner


class String(Runner):
    def execute(self, *args):
        return str(args[0])
