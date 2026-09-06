from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from client.shared.styles import DARK_STYLE, APP_STYLE
from client.views.news_view import NewsView
from client.views.chat_view import ChatView
from client.views.graph_view import GraphView
from client.views.setting_view import SettingsView
import sys

class MainWindow(QWidget):
    def __init__(self, user=None):
        super().__init__()
        self.setWindowTitle("AI News App")
        self.resize(1100, 700)
        self.user = user

        self.stack = QStackedWidget()
        self.news_view = NewsView(user=self.user)
        self.chat_view = ChatView(article=None)
        self.graph_view = GraphView()
        self.settings_view = SettingsView(user=self.user, parent=self)
        self.news_view.article_selection_changed.connect(self.update_chat_button)

        self.stack.addWidget(self.news_view)
        self.stack.addWidget(self.chat_view)
        self.stack.addWidget(self.graph_view)
        self.stack.addWidget(self.settings_view)

        self.menu_layout = QVBoxLayout()
        self.news_btn = QPushButton("📰 News")
        self.chat_btn = QPushButton("💬 Ask the AI")
        self.graph_btn = QPushButton("📊 Graphs")
        self.settings_btn = QPushButton("⚙ Settings")

        self.news_btn.setFixedWidth(180)
        self.chat_btn.setFixedWidth(180)
        self.graph_btn.setFixedWidth(180)
        self.settings_btn.setFixedWidth(180)

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
        layout.addWidget(self.stack, stretch=1)
        layout.addLayout(self.menu_layout)
        self.setLayout(layout)

        self.stack.setCurrentWidget(self.news_view)

        self.news_view.load_news()
        self.apply_theme(self.news_view.preferences.get("dark_mode", False))

    def update_chat_button(self, article):
        if article:
            self.chat_btn.setText("💬 Ask about article")
        else:
            self.chat_btn.setText("💬 Ask the AI")

    def apply_theme(self, dark_mode):
        self.style = DARK_STYLE if dark_mode else APP_STYLE
        self.setStyleSheet(self.style)
        self.news_view.setStyleSheet(self.style)
        self.chat_view.setStyleSheet(self.style)
        self.graph_view.setStyleSheet(self.style)
        self.settings_view.setStyleSheet(self.style)

        self.chat_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1dd2af,
                    stop:1 #1abc9c
                );
                border: 1px solid #129f85;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 5px;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.5);
                min-height: 28px;
            }
            QPushButton:pressed {
                background-color: #16a085;
                padding-top: 9px;
                padding-bottom: 7px;
            }
        """)

        self.update()

    def update_style(self):
        self.apply_theme(self.style == DARK_STYLE)

    def show_news(self):
        self.stack.setCurrentWidget(self.news_view)

    def show_chat(self):
        selected_article = self.news_view.selected_article
        self.chat_view.article = selected_article
        self.chat_view.question_box.clear()
        self.chat_view.answer_box.clear()
        self.stack.setCurrentWidget(self.chat_view)

    def show_graph(self):
        self.stack.setCurrentWidget(self.graph_view)

    def show_settings(self):
        self.stack.setCurrentWidget(self.settings_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(user={"id":1})
    window.show()
    sys.exit(app.exec())