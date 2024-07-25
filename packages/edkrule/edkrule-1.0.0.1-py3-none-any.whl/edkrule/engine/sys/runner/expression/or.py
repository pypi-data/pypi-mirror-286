from edkrule.engine.runner import Runner


class Or(Runner):
    def execute(self, *args):
        return args[0] or args[1]
