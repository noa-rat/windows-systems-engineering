# client/views/settings_view.py
# ממשק גרפי למסך ההגדרות (עריכת העדפות משתמש)

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QCheckBox, QMessageBox
from PySide6.QtCore import Qt
from client.shared.api import update_preferences, get_preferences
from client.shared.styles import APP_STYLE, DARK_STYLE

class SettingsView(QWidget):
    def __init__(self, user, parent=None):
        super().__init__()
        # משתמש נוכחי
        self.user = user
        # העדפות המשתמש הנוכחי
        self.preferences = get_preferences(user["id"])
        dark_mode = self.preferences.get("dark_mode", False)
        self.setStyleSheet(DARK_STYLE if dark_mode else APP_STYLE)
        # כותרת החלון
        self.setWindowTitle("User Preferences")
        # גודל החלון
        self.resize(400, 400)
        # חלון אב (כדי לאפשר חזרה למסך הקודם)
        self.parent_window = parent

        # פריסת רכיבים לאורך
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        title = QLabel("⚙ User Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin-bottom: 15px; font-weight: bold;")
        self.layout.addWidget(title)

        # קומבו-בוקס לבחירת קטגוריה
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet("font-size: 18px;")
        self.category_combo.addItems(["general", "technology", "sports", "health"])
        self.layout.addWidget(QLabel("Default News Category:"))
        self.layout.addWidget(self.category_combo)

        # צ'ק-בוקס לבחירת מצב בהיר/כהה
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.dark_mode_checkbox)

        # כפתור שמירת העדפות
        save_btn = QPushButton("💾 Save Changes")
        save_btn.clicked.connect(self.save_preferences)
        self.layout.addWidget(save_btn)

        # מאתחל ערכים נוכחיים
        self.load_preferences()

    # שולפת את העדפות המשתמש מהשרת וממלאת את השדות בהתאם
    def load_preferences(self):
        data = get_preferences(self.user["id"])
        if data:
            self.category_combo.setCurrentText(data.get("favorite_categories", ["general"])[0])
            self.dark_mode_checkbox.setChecked(data.get("dark_mode", False))

    # בונה מילון העדפות לפי מצב השדות ושולח בקשת עדכון לשרת
    def save_preferences(self):
        prefs = {
            "favorite_categories": [self.category_combo.currentText()],
            "dark_mode": self.dark_mode_checkbox.isChecked()
        }
        success = update_preferences(self.user["id"], prefs)
        if success:
            QMessageBox.information(self, "✅", "Preferences updated successfully.")
        else:
            QMessageBox.warning(self, "⚠️ Error", "Failed to update preferences.")