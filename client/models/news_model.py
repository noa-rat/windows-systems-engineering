# client/models/news_model.py
# ממדל מבנה של כתבה

# אובייקט מטיפוס כתבה
class NewsItem:
    def __init__(self, title: str, summary: str, fulltext: str, date: str, category: str = ""):
        self.title = title
        self.summary = summary
        self.fulltext = fulltext
        self.date = date
        self.category = category

    # ממיר אובייקט למחרוזת
    def __repr__(self):
        return f"<NewsItem '{self.title}' | {self.date}>"