from edkrule.atomic.atomic import Atomic


class AtomicInt(Atomic):
    def __init__(self, default: int = 0):
        super().__init__()
        self._value = default

    def increment(self, default: int = 1):
        with self._lock:
            self._value += default
            return self._value

    def decrement(self, default: int = 1):
        with self._lock:
            self._value -= default
            return self._value

    def get(self):
        with self._lock:
            return self._value
