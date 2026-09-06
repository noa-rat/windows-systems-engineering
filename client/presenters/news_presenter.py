from client.shared.api import refresh_news_async, get_preferences_async
from client.models.news_model import NewsItem

class NewsPresenter:
    def __init__(self, view):
        self.view = view

    def load_news(self, category, on_success, on_error):
        refresh_news_async(category, on_success, on_error)

    def load_preferences(self, user_id, on_success, on_error):
        get_preferences_async(user_id, on_success, on_error)