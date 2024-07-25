class TernaryStack:
    def __init__(self):
        self.stack = []

    def append(self, e):
        self.stack.append([e])

    def pop(self, index=-1):
        self.stack[index].pop()
        if len(self.stack[index]) == 0: self.stack.pop()

    def empty(self) -> bool:
        return len(self.stack) == 0
