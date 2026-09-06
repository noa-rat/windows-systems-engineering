import os

import requests
from dotenv import load_dotenv
from client.shared.async_tasks import run_async
from client.shared.cache import get_or_set, get_stale, set
from client.shared.http_client import get_session
from client.models.api_models import (
    ArticleResult,
    GraphResult,
    LoginResult,
    PreferencesResult,
    RegisterResult,
)

load_dotenv()

BASE_URL = os.getenv("AI_API_BASE_URL", "http://localhost:8000").rstrip("/")
VERIFY_TLS = os.getenv("AI_API_VERIFY_TLS", "true").lower() == "true"
_ACCESS_TOKEN = None
NEWS_CACHE_TTL = 300
PREFERENCES_CACHE_TTL = 60
GRAPH_CACHE_TTL = 300


def _json_response(response):
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", "The server rejected the request.")
        except ValueError:
            detail = response.text or "The server rejected the request."
        raise RuntimeError(f"HTTP {response.status_code}: {detail}")
    try:
        return response.json()
    except ValueError as error:
        raise RuntimeError("The server returned invalid JSON.") from error


def _get_json(url, *, params=None, timeout=15):
    response = get_session().get(
        url,
        params=params,
        headers=_auth_headers(),
        timeout=timeout,
        verify=VERIFY_TLS,
    )
    if response.status_code == 401:
        _clear_token()
    return _json_response(response)


def _clear_token():
    global _ACCESS_TOKEN
    _ACCESS_TOKEN = None


def _cached_get(key, ttl, request):
    try:
        return get_or_set(key, ttl, request)
    except (requests.RequestException, RuntimeError, ValueError):
        stale = get_stale(key)
        if stale is not None:
            return stale
        raise


def _auth_headers():
    if _ACCESS_TOKEN:
        return {"Authorization": f"Bearer {_ACCESS_TOKEN}"}
    return {}


def _store_token(response_data):
    global _ACCESS_TOKEN
    _ACCESS_TOKEN = response_data.get("access_token")

def login(username, password):
    try:
        res = get_session().post(
            f"{BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=15,
            verify=VERIFY_TLS,
        )
        data = _json_response(res)
        if data.get("success"):
            _store_token(data)
        return LoginResult.model_validate(data)
    except (requests.RequestException, RuntimeError) as e:
        print("Login failed:", e)
        return LoginResult(success=False, detail=str(e))

def register(username, password):
    try:
        res = get_session().post(
            f"{BASE_URL}/auth/register",
            json={"username": username, "password": password},
            timeout=15,
            verify=VERIFY_TLS,
        )
        return RegisterResult.model_validate(_json_response(res))
    except (requests.RequestException, RuntimeError) as e:
        print("Registration failed:", e)
        return RegisterResult(
            success=False,
            detail=f"Server communication failed: {e}",
        )

def get_news(category):
    data = _cached_get(
        f"news:{category}",
        NEWS_CACHE_TTL,
        lambda: _get_json(
            f"{BASE_URL}/news",
            params={"category": category},
            timeout=30
        ),
    )
    return [ArticleResult.model_validate(item) for item in data]

def search_news(keyword):
    data = _cached_get(
        f"search:{keyword.lower().strip()}",
        NEWS_CACHE_TTL,
        lambda: _get_json(
            f"{BASE_URL}/news/search",
            params={"q": keyword},
            timeout=30
        ),
    )
    return [ArticleResult.model_validate(item) for item in data]


def get_graph_statistics():
    data = _cached_get(
        "graphs:by-category",
        GRAPH_CACHE_TTL,
        lambda: _get_json(
            f"{BASE_URL}/graphs/by-category",
            timeout=15
        ),
    )
    return GraphResult(values={str(key): int(value) for key, value in data.items()})


def ask_ai(question, article=None):
    if article is not None and hasattr(article, "model_dump"):
        article = {
            "title": article.title,
            "summary": article.summary,
        }
    data = {
        "prompt": question,
        "article": article
    }
    response = get_session().post(
        f"{BASE_URL}/ask-ai",
        json=data,
        headers=_auth_headers(),
        timeout=130,
        verify=VERIFY_TLS,
    )
    return _json_response(response).get("answer", "")

def get_preferences(user_id):
    data = _cached_get(
        f"preferences:{user_id}",
        PREFERENCES_CACHE_TTL,
        lambda: _get_json(
            f"{BASE_URL}/auth/preferences",
            params={"user_id": user_id},
            timeout=15
        ),
    )
    return PreferencesResult.model_validate(data)

def update_preferences(user_id, prefs: dict):
    payload = {"user_id": user_id, **prefs}
    response = get_session().post(
        f"{BASE_URL}/auth/preferences",
        json=payload,
        headers=_auth_headers(),
        timeout=15,
        verify=VERIFY_TLS,
    )
    if response.status_code == 401:
        _clear_token()
    if response.status_code == 200:
        set(
            f"preferences:{user_id}",
            {"favorite_categories": prefs.get("favorite_categories", ["general"]),
             "dark_mode": prefs.get("dark_mode", False)},
        )
        return True
    _json_response(response)


def refresh_news(category):
    response = get_session().post(
        f"{BASE_URL}/news/refresh",
        params={"category": category},
        headers=_auth_headers(),
        timeout=130,
        verify=VERIFY_TLS,
    )
    data = _json_response(response)
    set(f"news:{category}", data)
    return [ArticleResult.model_validate(item) for item in data]


def login_async(username, password, on_success, on_error=None):
    run_async(lambda: login(username, password), on_success, on_error)


def register_async(username, password, on_success, on_error=None):
    run_async(lambda: register(username, password), on_success, on_error)


def get_news_async(category, on_success, on_error=None):
    run_async(lambda: get_news(category), on_success, on_error)


def refresh_news_async(category, on_success, on_error=None):
    run_async(lambda: refresh_news(category), on_success, on_error)


def search_news_async(keyword, on_success, on_error=None):
    run_async(lambda: search_news(keyword), on_success, on_error)


def get_graph_statistics_async(on_success, on_error=None):
    run_async(get_graph_statistics, on_success, on_error)


def ask_ai_async(question, article, on_success, on_error=None):
    run_async(lambda: ask_ai(question, article), on_success, on_error)


def get_preferences_async(user_id, on_success, on_error=None):
    run_async(lambda: get_preferences(user_id), on_success, on_error)


def update_preferences_async(user_id, prefs, on_success, on_error=None):
    run_async(lambda: update_preferences(user_id, prefs), on_success, on_error)