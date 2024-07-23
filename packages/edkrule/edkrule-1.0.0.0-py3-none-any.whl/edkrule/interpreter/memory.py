from edkrule.atomic.atomic_int import AtomicInt


class Memory:
    def __init__(self):
        self._cache = dict()
        self.order = AtomicInt()

    def add(self, op_ret: dict):
        for key in op_ret.keys():
            self._cache[key] = dict(order=self.order.increment(),
                                    value=op_ret.get(key).get("#ret"),
                                    name=op_ret.get(key).get("#name"))

    def set(self, key, value):
        self._cache[key]["value"] = value

    def get(self, key, default=None):
        return self._cache.get(key, default)

    def get_order(self, key):
        return self.get(key).get("order")
