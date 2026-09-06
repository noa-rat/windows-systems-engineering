from client.shared.api import ask_ai_async

class ChatPresenter:
    def __init__(self, view):
        self.view = view

    def ask_question(self, prompt, article, on_success, on_error):
        if not prompt.strip():
            on_error(ValueError("The question cannot be empty."))
            return
        ask_ai_async(prompt, article, on_success, on_error)