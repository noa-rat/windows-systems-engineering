from threading import local

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


_state = local()


def get_session():
    session = getattr(_state, "session", None)
    if session is None:
        retry = Retry(
            total=2,
            connect=2,
            read=2,
            backoff_factor=0.25,
            status_forcelist=(502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(
            pool_connections=8,
            pool_maxsize=16,
            max_retries=retry,
        )
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        _state.session = session
    return session
