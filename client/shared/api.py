# client/shared/api.py
# מרכז את התקשורת עם השרת

import requests

BASE_URL = "http://localhost:8000"

# בקשה להתחברות משתמש
def login(username, password):
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password}, timeout=15)
        print("🔍 RESPONSE:", res.status_code, res.text)
        return res.json()
    except Exception as e:
        print("❌ Login exception:", e)
        return {"success": False, "detail": str(e)}

# בקשה לרישום משתמש
def register(username, password):
    res = requests.post(f"{BASE_URL}/auth/register", json={"username": username, "password": password})
    return res.json()

# בקשה לשליפת כתבות לפי קטגוריה
def get_news(category):
    res = requests.get(f"{BASE_URL}/news", params={"category": category})
    return res.json()

# בקשה לשליפת כתבות לפי מילות מפתח
def search_news(keyword):
    res = requests.get(f"{BASE_URL}/news/search", params={"q": keyword})
    return res.json()

# שליחת שאלה ל-ollama
def ask_ai(question, article=None):
    data = {
        "prompt": question,
        "article": article
    }
    res = requests.post(f"{BASE_URL}/ask-ai", json=data)
    return res.json().get("answer", "")

# בקשה לקבלת העדפות משתמש
def get_preferences(user_id):
    try:
        res = requests.get(f"{BASE_URL}/auth/preferences", params={"user_id": user_id})
        if res.status_code == 200:
            return res.json()
        return {}
    except Exception as e:
        print("❌ Failed to fetch preferences:", e)
        return {}

# בקשה לעדכון העדפות משתמש
def update_preferences(user_id, prefs: dict):
    try:
        payload = {
            "user_id": user_id,
            **prefs
        }
        res = requests.post(f"{BASE_URL}/auth/preferences", json=payload)
        return res.status_code == 200
    except Exception as e:
        print("❌ Failed to update preferences:", e)
        return False