class Squeue:
    def __init__(self):
        self._data = []

    def append(self, e):
        self._data.append(e)

    @property
    def data(self) -> list:
        return self._data

    def get(self, i):
        return self._data[i]

    def top(self):
        if self.empty(): return None
        return self._data[0]

    def count(self): return len(self._data)

    def empty(self): return self.count() == 0
