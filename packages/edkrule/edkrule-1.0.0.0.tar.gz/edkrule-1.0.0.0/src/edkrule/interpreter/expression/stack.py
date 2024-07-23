from typing import Any


class Stack:
    def __init__(self):
        self._stack = []

    def push(self, e):
        self._stack.append(e)

    def pop(self):
        return self._stack.pop()

    def clear(self):
        self._stack.clear()

    def pops(self, count):
        pops = []
        while count > 0:
            pops.insert(0, self.pop())
            count -= 1
        return pops

    def pop_until(self, condition: Any, exclude_condition=True):
        pops = []
        while True:
            # pops.insert(0, self.pop())
            # if self.empty(): break
            if condition(self.top()):
                pops.insert(0, self.pop())
                if exclude_condition:
                    pops.pop(0)
                break
            else:
                pops.insert(0, self.pop())

        return pops

    def top(self, index: int = 0):
        if len(self._stack) == 0: return None
        return self._stack[index-1]

    def count(self):
        return len(self._stack)

    def empty(self):
        return self.count() == 0