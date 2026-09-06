# client/views/news_view.py
# ממשק גרפי למסך החדשות
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QPushButton, QTextEdit, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
from client.shared.styles import APP_STYLE, DARK_STYLE
from client.shared.api import get_news, get_preferences
from client.views.graph_view import GraphView
from client.views.chat_view import ChatView
from client.views.setting_view import SettingsView
from functools import partial
from client.presenters.news_presenter import NewsPresenter


class NewsView(QWidget):
    def __init__(self, user=None):
        super().__init__()
        # משתמש נוכחי
        self.user = user or {}
        # כותרת החלון
        self.setWindowTitle("AI News")
        # גודל החלון
        self.resize(800, 700)
        # רשימת הכתבות
        self.all_articles = None
        # הגדרת פרזנטור
        self.presenter = NewsPresenter(self)

        # פריסת רכיבים לאורך
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.title_label = QLabel("📰 AI News")
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # קומבו-בוקס לבחירת קטגוריה
        self.category_select = QComboBox()
        self.category_select.addItems(["general", "sports", "technology", "health"])
        self.layout.addWidget(self.category_select)

        # כפתור לטעינת כתבות חדשות
        self.load_button = QPushButton("Load News")
        self.load_button.clicked.connect(self.load_news)
        self.layout.addWidget(self.load_button)

        # חיפוש
        self.filtered = False
        # תיבה להזנת מילות החיפוש
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setFixedHeight(38)
        self.search_box.setStyleSheet("font-size: 18px; padding: 8px;")
        # כפתור חיפוש
        self.search_button = QPushButton("🔍")
        self.search_button.clicked.connect(self.on_search_click)
        # פריסה אופקית בין הכפתור לתיבת החיפוש
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_box, stretch=5)
        self.search_layout.addWidget(self.search_button, stretch=1)
        self.search_container = QWidget()
        self.search_container.setLayout(self.search_layout)
        self.layout.addWidget(self.search_container)

        # תיבה להצגת הכתבות
        self.news_box = QListWidget()
        self.layout.addWidget(self.news_box)
        # הכתבה הנבחרת
        self.selected_article = None

        # פונקצית עדכון מותאם אישית
        self.refresh_preferences()

    # טוענת את הכפתור לפי הקטגוריה הנבחרת ומציגה את הכתבות בתיבה
    def load_news(self):
        category = self.category_select.currentText()
        self.all_articles = self.presenter.load_news(category)
        self.news_box.clear()

        if not self.all_articles:
            item = QListWidgetItem()
            label = QLabel("No news found.")
            self.news_box.addItem(item)
            self.news_box.setItemWidget(item, label)
            return

        for i, article in enumerate(self.all_articles):
            html = (
                f"<h3>{article['title']}</h3>"
                f"<small>{article['date']}</small>"
                f"<p>{article['summary']}</p><hr>"
            )
            label = QLabel(html)
            label.setTextFormat(Qt.TextFormat.RichText)
            label.setWordWrap(True)
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # לוודא שהוא לא מתעלם
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction) # מאפשר לחיצה על טקסט
            label.setCursor(Qt.CursorShape.PointingHandCursor) # שינוי הסמן לגירוי משתמש
            label.mousePressEvent = partial(self.select_label, label=label, article=article)

            # עיטוף בתוך QWidget
            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.addWidget(label)

            item = QListWidgetItem()
            item.setSizeHint(wrapper.sizeHint())
            self.news_box.addItem(item)
            self.news_box.setItemWidget(item, wrapper)

    # בחירת כתבה
    def select_label(self, event, label, article):
        # אם כבר נבחרה כתבה (שונה), לא נאפשר בחירה נוספת
        if self.selected_article is not None and self.selected_article != article:
            return

        # לחיצה חוזרת על אותה כתבה – ביטול הבחירה
        if self.selected_article == article:
            self.selected_article = None
            label.setStyleSheet("")
        else:
            # בחירה חדשה
            self.selected_article = article
            label.setStyleSheet("background-color: #cce6ff; border-radius: 5px;")

    # מעדכנת עיצוב, קטגוריה וכתבות לפי העדפות המשתמש
    def refresh_preferences(self, if_load_news=True):
        self.preferences = self.presenter.load_preferences(self.user.get("id", 0)) or {}
        # עיצוב מחדש
        self.setStyleSheet(DARK_STYLE if self.preferences.get("dark_mode") else APP_STYLE)
        # קטגוריה מועדפת
        default_category = self.preferences.get("favorite_categories", ["general"])[0]
        if default_category in [self.category_select.itemText(i) for i in range(self.category_select.count())]:
            self.category_select.setCurrentText(default_category)
        # טעינה של הכתבות בהתאם לקטגוריה
        if if_load_news:
            self.load_news()

    # מסננת כתבות לפי תיבת החיפוש
    def filter_news(self):
        keyword = self.search_box.text().lower()
        if not keyword:
            return
        self.filtered = True
        self.news_box.clear()

        found_articles = []
        for article in self.all_articles:
            if keyword in article["title"].lower() or keyword in article["summary"].lower():
                found_articles.append(article)

        if not found_articles:
            item = QListWidgetItem()
            label = QLabel("No news matched your search.")
            self.news_box.addItem(item)
            self.news_box.setItemWidget(item, label)
        else:
            for article in found_articles:
                html = (
                    f"<h3>{article['title']}</h3>"
                    f"<small>{article['date']}</small>"
                    f"<p>{article['summary']}</p><hr>"
                )
                label = QLabel(html)
                label.setTextFormat(Qt.TextFormat.RichText)
                label.setWordWrap(True)
                label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)  # לוודא שהוא לא מתעלם
                label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)  # מאפשר לחיצה על טקסט
                label.setCursor(Qt.CursorShape.PointingHandCursor)  # שינוי הסמן לגירוי משתמש
                label.mousePressEvent = partial(self.select_label, label=label, article=article)

                # עיטוף בתוך QWidget
                wrapper = QWidget()
                layout = QVBoxLayout(wrapper)
                layout.setContentsMargins(6, 6, 6, 6)
                layout.addWidget(label)

                item = QListWidgetItem()
                item.setSizeHint(wrapper.sizeHint())
                self.news_box.addItem(item)
                self.news_box.setItemWidget(item, wrapper)

        # משנה את הכפתור לביטול הסינון
        self.search_button.setText("❌")

    # מחזירה את כלל הכתבות
    def clear_filter(self):
        self.filtered = False
        self.search_box.clear()
        self.news_box.clear()

        for article in self.all_articles:
            html = (
                f"<h3>{article['title']}</h3>"
                f"<small>{article['date']}</small>"
                f"<p>{article['summary']}</p><hr>"
            )
            label = QLabel(html)
            label.setTextFormat(Qt.TextFormat.RichText)
            label.setWordWrap(True)
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)  # לוודא שהוא לא מתעלם
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)  # מאפשר לחיצה על טקסט
            label.setCursor(Qt.CursorShape.PointingHandCursor)  # שינוי הסמן לגירוי משתמש
            label.mousePressEvent = partial(self.select_label, label=label, article=article)

            # עיטוף בתוך QWidget
            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.addWidget(label)

            item = QListWidgetItem()
            item.setSizeHint(wrapper.sizeHint())
            self.news_box.addItem(item)
            self.news_box.setItemWidget(item, wrapper)

        # משנה את הכפתור לחיפוש
        self.search_button.setText("🔍")

    # מפעילה את החיפוש לפי מצב הכפתור
    def on_search_click(self):
        if self.search_button.text() == "🔍":
            self.filter_news()
        else:
            self.clear_filter()