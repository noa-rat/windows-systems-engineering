
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QCheckBox, QMessageBox
from PySide6.QtCore import Qt
from client.shared.api import get_preferences_async, update_preferences_async
from client.shared.styles import APP_STYLE, DARK_STYLE

class SettingsView(QWidget):
    def __init__(self, user, parent=None):
        super().__init__()
        self.user = user
        self.preferences = {}
        dark_mode = False
        self.setStyleSheet(DARK_STYLE if dark_mode else APP_STYLE)
        self.setWindowTitle("User Preferences")
        self.resize(400, 400)
        self.parent_window = parent

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(36, 28, 36, 28)
        self.layout.setSpacing(14)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        title = QLabel("⚙ User Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18pt; margin-bottom: 15px; font-weight: bold;")
        self.layout.addWidget(title)

        self.category_combo = QComboBox()
        self.category_combo.setFixedHeight(42)
        self.category_combo.addItems(["general", "technology", "sports", "health"])
        self.layout.addWidget(QLabel("Default News Category:"))
        self.layout.addWidget(self.category_combo)

        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.setMinimumHeight(32)
        self.layout.addWidget(self.dark_mode_checkbox)

        self.save_button = QPushButton("💾 Save Changes")
        self.save_button.setMinimumHeight(44)
        self.save_button.clicked.connect(self.save_preferences)
        self.layout.addWidget(self.save_button)

        self.load_preferences()

    def load_preferences(self):
        get_preferences_async(
            self.user["id"],
            self._preferences_loaded,
            self._preferences_load_failed
        )

    def _preferences_loaded(self, data):
        data = data or {}
        self.preferences = data
        if data:
            self.category_combo.setCurrentText(data.get("favorite_categories", ["general"])[0])
            self.dark_mode_checkbox.setChecked(data.get("dark_mode", False))

    def _preferences_load_failed(self, error):
        print("Failed to load preferences:", error)

    def save_preferences(self):
        prefs = {
            "favorite_categories": [self.category_combo.currentText()],
            "dark_mode": self.dark_mode_checkbox.isChecked()
        }
        self.save_button.setEnabled(False)
        update_preferences_async(
            self.user["id"],
            prefs,
            lambda success: self._save_completed(success, prefs),
            self._save_failed
        )

    def _save_completed(self, success, prefs):
        self.save_button.setEnabled(True)
        if success:
            if self.parent_window is not None and hasattr(self.parent_window, "apply_theme"):
                self.parent_window.apply_theme(prefs["dark_mode"])
            else:
                self.setStyleSheet(DARK_STYLE if prefs["dark_mode"] else APP_STYLE)
            QMessageBox.information(self, "✅", "Preferences updated successfully.")
        else:
            QMessageBox.warning(self, "⚠️ Error", "Failed to update preferences.")

    def _save_failed(self, error):
        self.save_button.setEnabled(True)
        print("Failed to save preferences:", error)
        QMessageBox.warning(self, "⚠️ Error", "Failed to update preferences.")