# client/presenters/graph_presenter.py
# מנהל את התקשורת בין מסך הגרפים לשרת

from client.shared.api import get_news
import requests

class GraphPresenter:
    def __init__(self):
        # מאפשר תקשורת עם השרת
        self.api_url = "http://localhost:8000/graphs/by-category"

    # מחשב כמות כתבות בכל קטגוריה
    def get_data_by_category(self):
        data = get_news("general")
        stats = {}
        for item in data:
            cat = item.get("category", "unknown")
            stats[cat] = stats.get(cat, 0) + 1
        return stats

    # שולח בקשה לשרת לקבלת הגרף
    def fetch_category_data(self):
        try:
            res = requests.get(self.api_url)
            return res.json()
        except Exception as e:
            print("שגיאה בשליפת גרף:", e)
            return {}