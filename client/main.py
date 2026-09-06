# cd "C:\Users\WIN 11\Desktop\Windows Systems Engineering"
# .\.venv\Scripts\python.exe -m client.main

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from client.views.login_view import LoginView
import sys


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))

    window = LoginView()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()