# client/views/chat_view.py
# ממשק גרפי למסך הצ'אט

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Qt

from client.presenters.chat_presenter import ChatPresenter
from client.shared.styles import APP_STYLE, DARK_STYLE
from client.shared.api import ask_ai

class ChatView(QWidget):
    def __init__(self, parent=None, article=None, style=APP_STYLE):
        super().__init__()
        # כתבה נבחרת (אם ישנה)
        self.article = article
        # סגנון עיצוב אחיד
        self.setStyleSheet(style)
        # כותרת החלון
        self.setWindowTitle("Ask the AI")
        # גודל החלון
        self.resize(400, 400)
        # חלון אב (כדי לאפשר חזרה למסך הקודם)
        self.parent_window = parent
        # הגדרת פרזנטור
        self.presenter = ChatPresenter(view=self)

        # פריסת רכיבים לאורך
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.title = QLabel("💬 AI Assistant")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # תיבה להזנת שאלה
        self.question_box = QTextEdit()
        self.question_box.setPlaceholderText("Type your question here...")
        self.question_box.setFixedHeight(200)
        self.layout.addWidget(self.question_box)

        # תיבת להצגת התשובה
        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setFixedHeight(400)
        self.layout.addWidget(self.answer_box)

        # כפתור לשליחת השאלה
        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.handle_question)
        self.layout.addWidget(self.ask_button)

    # קוראת את טקסט השאלה ושולחת אותו לשרת
    def handle_question(self):
        prompt = self.question_box.toPlainText()
        answer = self.presenter.ask_question(prompt, self.article)
        self.answer_box.setPlainText(answer)