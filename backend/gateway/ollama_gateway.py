# backend/gateway/ollama_gateway.py
# מנהל תקשורת עם ollama

import subprocess
from backend.config import settings

# מסכם כתבות עם ollama
def summarize_with_ollama(text):
    print("🧠 שולח טקסט לסיכום ל־Ollama...")
    # בקשה לסיכום + תוכן הכתבה
    prompt = f"Summarize this news article in a short, clear paragraph:\n\n{text}"
    summary = ask_ollama(prompt)
    print("✅ סיכום התקבל מ־Ollama.")
    return summary

# שולח שאלה חופשית
def ask_ollama(prompt):
    try:
        # מריץ את הפקודה
        result = subprocess.run(
            ["ollama", "run", settings.OLLAMA_MODEL],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )

        if result.stderr:
            print("⚠️ STDERR:", result.stderr.decode("utf-8"))

        # קורא את תשובת המודל
        answer = result.stdout.decode("utf-8").strip()
        return answer

    except Exception as e:
        print("❌ שגיאה במהלך שיחה עם Ollama:", e)
        return "AI response failed."