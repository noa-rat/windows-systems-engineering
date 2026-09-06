from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, status


_lock = Lock()
_events = defaultdict(deque)
_WINDOW_SECONDS = 60
_CHAT_REQUESTS_PER_USER = 20


def enforce_chat_quota(user_id: int):
    now = monotonic()
    key = str(user_id)
    with _lock:
        events = _events[key]
        while events and now - events[0] > _WINDOW_SECONDS:
            events.popleft()
        if len(events) >= _CHAT_REQUESTS_PER_USER:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Chat request limit reached. Please try again later.",
            )
        events.append(now)
