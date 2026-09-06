from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal


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
            self.signals.succeeded.emit(self.function())
        except Exception as error:
            self.signals.failed.emit(error)


def run_async(function, on_success, on_error=None):
    worker = _Worker(function)
    worker.signals.succeeded.connect(on_success)
    if on_error is not None:
        worker.signals.failed.connect(on_error)
    QThreadPool.globalInstance().start(worker)
