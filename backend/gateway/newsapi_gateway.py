# backend/gateway/newsapi_gateway.py
# מנהל תקשורת עם NewsAPI.org

import requests
from backend.config import settings

# שולח בקשה ל-NewsAPI ומחזיר את הכתבות
def fetch_from_newsapi(category="general", page_size=5):
    print(f"🔎 מביא חדשות מ־NewsAPI בקטגוריה: {category}")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": settings.NEWS_API_KEY,
        "language": "en",
        "pageSize": page_size,
        "category": category
    }

    try:
        # שולח בקשה לשירות
        response = requests.get(url, params=params)
        # טיפול בשגיאות
        response.raise_for_status()
        # מחלץ את רשימת הכתבות מתוך התשובה
        articles = response.json().get("articles", [])
        print(f"📥 התקבלו {len(articles)} כתבות.")
        return articles

    except requests.RequestException as e:
        print("❌ שגיאה בקריאת NewsAPI:", e)
        return []