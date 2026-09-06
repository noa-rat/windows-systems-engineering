# backend/models/user_model.py
# ממדל מבנה של משתמש

# אובייקט מטיפוס משתמש
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    # ממיר את האובייקט לטיפוס מילון
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }