from threading import Lock
from time import monotonic


class CircuitBreaker:
    def __init__(self, name, failure_threshold=3, recovery_seconds=30):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_seconds = recovery_seconds
        self._failures = 0
        self._opened_at = None
        self._lock = Lock()

    def before_call(self):
        with self._lock:
            if self._opened_at is None:
                return
            if monotonic() - self._opened_at >= self.recovery_seconds:
                self._opened_at = None
                self._failures = 0
                return
            raise RuntimeError(f"{self.name} is temporarily unavailable.")

    def success(self):
        with self._lock:
            self._failures = 0
            self._opened_at = None

    def failure(self):
        with self._lock:
            self._failures += 1
            if self._failures >= self.failure_threshold:
                self._opened_at = monotonic()
