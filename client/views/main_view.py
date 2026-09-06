from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Signal

from client.shared.styles import APP_STYLE, DARK_STYLE
from client.views.chat_view import ChatView
from client.views.graph_view import GraphView
from client.views.news_view import NewsView
from client.views.setting_view import SettingsView


class MainWindow(QWidget):
    ready = Signal()

    def __init__(self, user=None):
        super().__init__()
        self.setWindowTitle("AI News App")
        self.resize(1100, 700)
        self.setMinimumSize(850, 560)
        self.user = user
        self.is_ready = False

        self.stack = QStackedWidget()
        self.news_view = NewsView(user=self.user, auto_load_preferences=False)
        self.news_view.parent_window = self
        self.chat_view = ChatView(article=None)
        self.graph_view = GraphView()
        self.settings_view = SettingsView(user=self.user, parent=self)
        self.news_view.article_selection_changed.connect(self.update_chat_button)
        self.news_view.preferences_loaded.connect(self._initial_preferences_ready)

        self.stack.addWidget(self.news_view)
        self.stack.addWidget(self.chat_view)
        self.stack.addWidget(self.graph_view)
        self.stack.addWidget(self.settings_view)

        self.menu_panel = QFrame()
        self.menu_panel.setObjectName("navigationPanel")
        self.menu_panel.setFixedWidth(220)
        self.menu_layout = QVBoxLayout(self.menu_panel)
        self.menu_layout.setContentsMargins(12, 16, 12, 16)
        self.menu_layout.setSpacing(10)

        self.news_btn = self._create_nav_button("News")
        self.chat_btn = self._create_nav_button("Ask the AI")
        self.graph_btn = self._create_nav_button("Graphs")
        self.settings_btn = self._create_nav_button("Settings")

        self.news_btn.clicked.connect(self.show_news)
        self.chat_btn.clicked.connect(self.show_chat)
        self.graph_btn.clicked.connect(self.show_graph)
        self.settings_btn.clicked.connect(self.show_settings)

        self.menu_layout.addWidget(self.news_btn)
        self.menu_layout.addWidget(self.chat_btn)
        self.menu_layout.addWidget(self.graph_btn)
        self.menu_layout.addWidget(self.settings_btn)
        self.menu_layout.addStretch()

        layout = QHBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        layout.addWidget(self.stack, stretch=1)
        layout.addWidget(self.menu_panel)
        self.setLayout(layout)

        self.stack.setCurrentWidget(self.news_view)
        self.news_btn.setChecked(True)
        self.news_view.refresh_preferences(False)

    def _initial_preferences_ready(self, dark_mode):
        if self.is_ready:
            return
        self.apply_theme(dark_mode)
        self.news_view.load_stored_news()
        self.is_ready = True
        self.ready.emit()

    @staticmethod
    def _create_nav_button(text):
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setMinimumHeight(48)
        return button

    def _set_active_button(self, active_button):
        for button in (
            self.news_btn,
            self.chat_btn,
            self.graph_btn,
            self.settings_btn,
        ):
            button.setChecked(button is active_button)

    def update_chat_button(self, article):
        self.chat_btn.setText("Ask about article" if article else "Ask the AI")

    def apply_theme(self, dark_mode):
        self.style = DARK_STYLE if dark_mode else APP_STYLE
        self.setStyleSheet(self.style)
        for view in (
            self.news_view,
            self.chat_view,
            self.graph_view,
            self.settings_view,
        ):
            view.setStyleSheet(self.style)
        self.graph_view.apply_theme(dark_mode)
        self.update()

    def update_style(self):
        self.apply_theme(self.style == DARK_STYLE)

    def show_news(self):
        self._set_active_button(self.news_btn)
        self.stack.setCurrentWidget(self.news_view)

    def show_chat(self):
        self._set_active_button(self.chat_btn)
        self.chat_view.article = self.news_view.selected_article
        self.chat_view.question_box.clear()
        self.chat_view.answer_box.clear()
        self.stack.setCurrentWidget(self.chat_view)

    def show_graph(self):
        self._set_active_button(self.graph_btn)
        self.stack.setCurrentWidget(self.graph_view)

    def show_settings(self):
        self._set_active_button(self.settings_btn)
        self.stack.setCurrentWidget(self.settings_view)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow(user={"id": 1})
    window.ready.connect(window.show)
    if window.is_ready:
        window.show()
    sys.exit(app.exec())
