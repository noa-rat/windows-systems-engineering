from client.shared.api import login_async, register_async

class LoginPresenter:
    def __init__(self, view):
        self.view = view

    def attempt_login(self, username, password, on_success, on_error):
        if not username or not password:
            on_success({"success": False, "detail": "Username and password are required."})
            return
        login_async(username, password, on_success, on_error)

    def attempt_register(self, username, password, on_success, on_error):
        if not username or not password:
            on_success({"success": False, "detail": "Username and password are required."})
            return
        register_async(username, password, on_success, on_error)