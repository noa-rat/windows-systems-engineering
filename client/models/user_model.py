# client/models/user_model.py
# ממדל מבנה של משתמש

# אובייקט מטיפוס משתמש (כולל העדפות)
class User:
    def __init__(self, user_id: int, username: str, preferences: dict = None):
        self.user_id = user_id
        self.username = username
        self.preferences = preferences or {
            "dark_mode": False,
            "favorite_categories": []
        }

    # ממיר את האובייקט למחרוזת
    def __repr__(self):
        return f"<User {self.username} | ID: {self.user_id}>"