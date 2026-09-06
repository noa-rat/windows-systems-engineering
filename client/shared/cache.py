from threading import Event, Lock
from time import monotonic


_entries = {}
_inflight = {}
_lock = Lock()


def get(key, max_age):
    with _lock:
        entry = _entries.get(key)
        if entry is None:
            return None
        value, created = entry
        if monotonic() - created <= max_age:
            return value
        return None


def get_stale(key):
    with _lock:
        entry = _entries.get(key)
        return entry[0] if entry is not None else None


def set(key, value):
    with _lock:
        _entries[key] = (value, monotonic())


def get_or_set(key, max_age, request):
    cached = get(key, max_age)
    if cached is not None:
        return cached

    with _lock:
        event = _inflight.get(key)
        if event is None:
            event = {
                "done": False,
                "value": None,
                "error": None,
                "signal": Event(),
            }
            _inflight[key] = event
            owner = True
        else:
            owner = False

    if not owner:
        while True:
            with _lock:
                if event["done"]:
                    if event["error"] is not None:
                        raise event["error"]
                    return event["value"]
            event["signal"].wait()

    try:
        value = request()
        set(key, value)
        with _lock:
            event["value"] = value
        return value
    except Exception as error:
        with _lock:
            event["error"] = error
        raise
    finally:
        with _lock:
            event["done"] = True
            _inflight.pop(key, None)
            event["signal"].set()


def delete(key):
    with _lock:
        _entries.pop(key, None)
