# client/presenters/news_presenter.py
# מנהל את התקשורת בין מסך החדשות לשרת

from client.shared.api import get_news, get_preferences
from client.models.news_model import NewsItem

class NewsPresenter:
    # מאפשר תקשורת עם ממשק המשתמש
    def __init__(self, view):
        self.view = view

    # שולח בקשה לשרת לקבל כתבות לפי קטגוריה
    def load_news(self, category):
        return get_news(category)

    # שולח בקשה לשרת לקבל העדפות משתמש
    def load_preferences(self, user_id):
        return get_preferences(user_id)