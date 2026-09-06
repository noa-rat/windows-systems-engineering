import requests
from backend.config import settings
from backend.models.api_models import NewsApiArticle
from backend.services.circuit_breaker import CircuitBreaker


_newsapi_breaker = CircuitBreaker("NewsAPI")


def fetch_from_newsapi(category="general", page_size=5):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": settings.NEWS_API_KEY,
        "language": "en",
        "pageSize": min(page_size, settings.NEWS_MAX_ARTICLES),
        "category": category
    }

    _newsapi_breaker.before_call()
    try:
        response = requests.get(
            url,
            params=params,
            timeout=settings.NEWS_API_TIMEOUT,
        )
        response.raise_for_status()
        result = [
            NewsApiArticle.model_validate(article)
            for article in response.json().get("articles", [])
        ]
        _newsapi_breaker.success()
        return result
    except (requests.RequestException, ValueError):
        _newsapi_breaker.failure()
        raise