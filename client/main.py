# client/main.py
# מפעיל את הלקוח

from PySide6.QtWidgets import QApplication
from client.views.login_view import LoginView
import sys


def main():
    app = QApplication(sys.argv)

    # פותח את חלון ההתחברות
    window = LoginView()
    window.show()

    # מפעיל את הלולאה הראשית ומבטיח סגירה תקינה
    sys.exit(app.exec())

if __name__ == "__main__":
    main()