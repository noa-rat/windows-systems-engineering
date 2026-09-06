# backend/models/news_model.py
# ממדל מבנה של כתבה

# אובייקט מטיפוס כתבה
class NewsItem:
    def __init__(self, title, fulltext, summary, category, date):
        self.title = title
        self.fulltext = fulltext
        self.summary = summary
        self.category = category
        self.date = date

    # ממיר את האובייקט לטיפוס מילון
    def to_dict(self):
        return {
            "title": self.title,
            "fulltext": self.fulltext,
            "summary": self.summary,
            "category": self.category,
            "date": self.date
        }