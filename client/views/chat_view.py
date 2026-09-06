
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Qt

from client.presenters.chat_presenter import ChatPresenter
from client.shared.styles import APP_STYLE, DARK_STYLE
from client.shared.api import ask_ai

class ChatView(QWidget):
    def __init__(self, parent=None, article=None, style=APP_STYLE):
        super().__init__()
        self.article = article
        self.setStyleSheet(style)
        self.setWindowTitle("Ask the AI")
        self.resize(400, 400)
        self.parent_window = parent
        self.presenter = ChatPresenter(view=self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("💬 AI Assistant")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.question_box = QTextEdit()
        self.question_box.setPlaceholderText("Type your question here...")
        self.question_box.setFixedHeight(200)
        self.layout.addWidget(self.question_box)

        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setFixedHeight(400)
        self.layout.addWidget(self.answer_box)

        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.handle_question)
        self.layout.addWidget(self.ask_button)

    def handle_question(self):
        prompt = self.question_box.toPlainText()
        self.ask_button.setEnabled(False)
        self.ask_button.setText("Thinking...")
        self.presenter.ask_question(
            prompt,
            self.article,
            self._answer_received,
            self._answer_failed
        )

    def _answer_received(self, answer):
        self.ask_button.setEnabled(True)
        self.ask_button.setText("Ask")
        self.answer_box.setPlainText(answer)

    def _answer_failed(self, error):
        self.ask_button.setEnabled(True)
        self.ask_button.setText("Ask")
        self.answer_box.setPlainText(f"Request failed: {error}")