from edkrule.engine.runner import Runner


class Boolean(Runner):
    def execute(self, *args):
        if args[0].lower() == 'true': return True
        if args[0].lower() == 'false': return False
