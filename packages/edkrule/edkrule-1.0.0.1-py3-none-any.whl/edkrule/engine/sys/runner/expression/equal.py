from edkrule.engine.runner import Runner


class Equal(Runner):
    def execute(self, *args):
        return args[0] == args[1]
