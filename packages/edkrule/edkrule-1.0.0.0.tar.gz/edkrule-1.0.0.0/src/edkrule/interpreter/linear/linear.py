from edkrule.atomic.atomic_int import AtomicInt


class Linear:
    def __init__(self):
        self._list = list()
        self._point = AtomicInt(-1)
        self._length = AtomicInt()

    def reset(self):
        self._length = AtomicInt(len(self._list))
        self._point = AtomicInt(-1)

    def length(self) -> int: return self._length.get()

    def completed(self) -> bool:
        return self.length() == 0

    def clean(self):
        self._list = list()
        self.reset()
