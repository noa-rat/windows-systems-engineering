
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
        self.setStyleSheet(APP_STYLE)
        self.setWindowTitle("Login - AI News")
        self.resize(400, 400)
        self.presenter = LoginPresenter(self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("👋\nWelcome\nto AI News")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24pt; font-weight: bold; margin-bottom: 18px;")
        self.layout.addWidget(self.title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("font-size: 13pt; padding: 8px;")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("font-size: 13pt; padding: 8px;")
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_register)
        self.layout.addWidget(self.register_button)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self._set_auth_buttons_enabled(False)
        self.presenter.attempt_login(
            username,
            password,
            self._login_completed,
            self._request_failed
        )

    def _login_completed(self, result):
        self._set_auth_buttons_enabled(True)
        if result.get("success"):
            self.main_window = MainWindow(user=result["user"])
            self.main_window.ready.connect(self._show_main_window)
            if self.main_window.is_ready:
                self._show_main_window()
        else:
            QMessageBox.warning(self, "Login Failed", result.get("detail", "Unknown error."))

    def _show_main_window(self):
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.close()

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self._set_auth_buttons_enabled(False)
        self.presenter.attempt_register(
            username,
            password,
            self._register_completed,
            self._request_failed
        )

    def _register_completed(self, result):
        self._set_auth_buttons_enabled(True)
        if result.get("success"):
            QMessageBox.information(self, "Success", "User registered! You can now log in.")
        else:
            QMessageBox.warning(self, "Register Failed", result.get("detail", "Unknown error."))

    def _request_failed(self, error):
        self._set_auth_buttons_enabled(True)
        QMessageBox.warning(self, "Communication Error", str(error))

    def _set_auth_buttons_enabled(self, enabled):
        self.login_button.setEnabled(enabled)
        self.register_button.setEnabled(enabled)