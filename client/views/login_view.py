# client/views/login_view.py
# ממשק גרפי למסך ההתחברות

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from client.shared.api import login, register
from client.shared.styles import APP_STYLE
from client.views.main_view import MainWindow
from client.views.news_view import NewsView
from client.presenters.login_presenter import LoginPresenter

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        # סגנון עיצוב אחיד
        self.setStyleSheet(APP_STYLE)
        # כותרת החלון
        self.setWindowTitle("Login - AI News")
        # גודל החלון
        self.resize(400, 400)
        # הגדרת פרזנטור
        self.presenter = LoginPresenter(self)

        # פריסת רכיבים לאורך
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.title = QLabel("👋\nWelcome\nto AI News")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 18px;")
        self.layout.addWidget(self.title)

        # תיבה להזנת שם משתמש
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("font-size: 18px; padding: 8px;")
        self.layout.addWidget(self.username_input)

        # תיבת להזנת סיסמה
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("font-size: 18px; padding: 8px;")
        self.layout.addWidget(self.password_input)

        # כפתור להתחברות
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_button)

        # כפתור להרשמה
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_register)
        self.layout.addWidget(self.register_button)

    # קוראת את שם המשתמש והסיסמה שהוזנו ושולחת בקשת התחברות לשרת
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        result = self.presenter.attempt_login(username, password)
        if result.get("success"):
            # פותח את חלון החדשות
            self.main_window = MainWindow(user=result["user"])
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", result.get("detail", "Unknown error."))

    # קוראת את שם המשתמש והסיסמה שהוזנו ושולחת בקשת הרשמה לשרת
    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        result = self.presenter.attempt_register(username, password)
        if result.get("success"):
            QMessageBox.information(self, "Success", "User registered! You can now log in.")
        else:
            QMessageBox.warning(self, "Register Failed", result.get("detail", "Unknown error."))