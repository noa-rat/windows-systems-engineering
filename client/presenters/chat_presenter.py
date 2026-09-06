# client/presenters/chat_presenter.py
# מנהל את התקשורת בין מסך הצ'אט לשרת

from client.shared.api import ask_ai

class ChatPresenter:
    # מאפשר תקשורת עם ממשק המשתמש
    def __init__(self, view):
        self.view = view

    # מעביר את השאלה שהזין המשתמש ל-ollama
    def ask_question(self, prompt, article=None):
        if not prompt.strip():
            return "שאלה לא יכולה להיות ריקה."
        return ask_ai(prompt, article)