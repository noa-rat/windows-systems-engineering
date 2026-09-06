from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QPushButton, QTextEdit, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt, Signal
from client.shared.styles import APP_STYLE, DARK_STYLE
from client.views.graph_view import GraphView
from client.views.chat_view import ChatView
from client.views.setting_view import SettingsView
from functools import partial
from client.presenters.news_presenter import NewsPresenter


class NewsView(QWidget):
    article_selection_changed = Signal(object)

    def __init__(self, user=None):
        super().__init__()
        self.user = user or {}
        self.setWindowTitle("AI News")
        self.resize(800, 700)
        self.all_articles = []
        self.preferences = {}
        self.presenter = NewsPresenter(self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("📰 AI News")
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.category_select = QComboBox()
        self.category_select.addItems(["general", "sports", "technology", "health"])
        self.layout.addWidget(self.category_select)

        self.load_button = QPushButton("Load News")
        self.load_button.clicked.connect(self.load_news)
        self.layout.addWidget(self.load_button)

        self.filtered = False
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setFixedHeight(38)
        self.search_box.setStyleSheet("font-size: 18px; padding: 8px;")
        self.search_button = QPushButton("🔍")
        self.search_button.clicked.connect(self.on_search_click)
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_box, stretch=5)
        self.search_layout.addWidget(self.search_button, stretch=1)
        self.search_container = QWidget()
        self.search_container.setLayout(self.search_layout)
        self.layout.addWidget(self.search_container)

        self.news_box = QListWidget()
        self.layout.addWidget(self.news_box)
        self.selected_article = None

        self.refresh_preferences(False)

    def load_news(self):
        category = self.category_select.currentText()
        self.load_button.setEnabled(False)
        self.load_button.setText("Loading...")
        self.presenter.load_news(category, self._news_loaded, self._news_load_failed)

    def _news_loaded(self, articles):
        self.load_button.setEnabled(True)
        self.load_button.setText("Load News")
        self.all_articles = articles or []
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
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = partial(self.select_label, label=label, article=article)

            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.addWidget(label)

            item = QListWidgetItem()
            item.setSizeHint(wrapper.sizeHint())
            self.news_box.addItem(item)
            self.news_box.setItemWidget(item, wrapper)

    def _news_load_failed(self, error):
        self.load_button.setEnabled(True)
        self.load_button.setText("Load News")
        print("Failed to load news:", error)
        self.news_box.clear()
        item = QListWidgetItem()
        label = QLabel("Failed to load news.")
        self.news_box.addItem(item)
        self.news_box.setItemWidget(item, label)

    def select_label(self, event, label, article):
        if self.selected_article is not None and self.selected_article != article:
            return

        if self.selected_article == article:
            self.selected_article = None
            label.setStyleSheet("")
            self.article_selection_changed.emit(None)
        else:
            self.selected_article = article
            label.setStyleSheet("background-color: #cce6ff; border-radius: 5px;")
            self.article_selection_changed.emit(article)

    def refresh_preferences(self, if_load_news=False):
        self.presenter.load_preferences(
            self.user.get("id", 0),
            lambda data: self._preferences_loaded(data, if_load_news),
            self._preferences_load_failed
        )

    def _preferences_loaded(self, data, if_load_news):
        self.preferences = data or {}
        self.setStyleSheet(DARK_STYLE if self.preferences.get("dark_mode") else APP_STYLE)
        default_category = self.preferences.get("favorite_categories", ["general"])[0]
        if default_category in [self.category_select.itemText(i) for i in range(self.category_select.count())]:
            self.category_select.setCurrentText(default_category)
        if if_load_news:
            self.load_news()

    def _preferences_load_failed(self, error):
        print("Failed to load preferences:", error)

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
                label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
                label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                label.setCursor(Qt.CursorShape.PointingHandCursor)
                label.mousePressEvent = partial(self.select_label, label=label, article=article)

                wrapper = QWidget()
                layout = QVBoxLayout(wrapper)
                layout.setContentsMargins(6, 6, 6, 6)
                layout.addWidget(label)

                item = QListWidgetItem()
                item.setSizeHint(wrapper.sizeHint())
                self.news_box.addItem(item)
                self.news_box.setItemWidget(item, wrapper)

        self.search_button.setText("❌")

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
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = partial(self.select_label, label=label, article=article)

            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.addWidget(label)

            item = QListWidgetItem()
            item.setSizeHint(wrapper.sizeHint())
            self.news_box.addItem(item)
            self.news_box.setItemWidget(item, wrapper)

        self.search_button.setText("🔍")

    def on_search_click(self):
        if self.search_button.text() == "🔍":
            self.filter_news()
        else:
            self.clear_filter()