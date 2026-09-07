from threading import Lock

from PySide6.QtCore import QCoreApplication, QObject, QRunnable, QThreadPool, Signal


class _WorkerSignals(QObject):
    succeeded = Signal(object)
    failed = Signal(object)


class _Worker(QRunnable):
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.signals = _WorkerSignals()

    def run(self):
        try:
            result = self.function()
            if not QCoreApplication.closingDown():
                self.signals.succeeded.emit(result)
        except Exception as error:
            if not QCoreApplication.closingDown():
                self.signals.failed.emit(error)


_active_workers = set()
_workers_lock = Lock()


def _release_worker(worker):
    with _workers_lock:
        _active_workers.discard(worker)


def run_async(function, on_success, on_error=None):
    worker = _Worker(function)
    with _workers_lock:
        _active_workers.add(worker)

    def handle_success(result):
        try:
            on_success(result)
        finally:
            _release_worker(worker)

    def handle_error(error):
        try:
            if on_error is not None:
                on_error(error)
        finally:
            _release_worker(worker)

    worker.signals.succeeded.connect(handle_success)
    if on_error is not None:
        worker.signals.failed.connect(handle_error)
    QThreadPool.globalInstance().start(worker)
