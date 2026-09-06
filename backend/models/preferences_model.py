# backend/models/preferences_model.py
# ממדל מבנה של העדפות משתמש

# אובייקט מטיפוס העדפות משתמש
class UserPreferences:
    def __init__(self, user_id, dark_mode=False, favorite_categories=None):
        self.user_id = user_id
        self.dark_mode = dark_mode
        self.favorite_categories = favorite_categories

    # ממיר את האובייקט לטיפוס מילון
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "dark_mode": self.dark_mode,
            "favorite_categories": self.favorite_categories
        }