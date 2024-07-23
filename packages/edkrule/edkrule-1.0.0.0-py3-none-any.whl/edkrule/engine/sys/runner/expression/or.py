from edkrule.engine.runner import Runner


class Or(Runner):
    def run(self, *args):
        return args[0] or args[1]
