import threading


class Atomic:
    def __init__(self):
        self._lock = threading.Lock()
