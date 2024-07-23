from edkrule.engine.runner import Runner


class String(Runner):
    def run(self, *args):
        return str(args[0])
