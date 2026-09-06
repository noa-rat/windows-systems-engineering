# client/presenters/login_presenter.py
# מנהל את התקשורת בין מסך ההתחברות לשרת

from client.shared.api import login, register

class LoginPresenter:
    # מאפשר תקשורת עם ממשק המשתמש
    def __init__(self, view):
        self.view = view

    # מאמת את נתוני המשתמש ושולח בקשת התחברות לשרת
    def attempt_login(self, username, password):
        if not username or not password:
            return {"success": False, "detail": "יש להזין שם משתמש וסיסמה."}
        return login(username, password)

    # מאמת את נתוני המשתמש ושולח בקשת הרשמה לשרת
    def attempt_register(self, username, password):
        if not username or not password:
            return {"success": False, "detail": "שם משתמש וסיסמה נחוצים."}
        return register(username, password)