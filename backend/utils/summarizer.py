# backend/utils/summarizer.py
# פונקציות שימושיות לטיפול במחרוזות

from datetime import datetime

# מגביל אורך מחרוזת ל-60 מילים כברירת מחדל
def truncate_text(text, max_words=60):
    words = text.split()
    return " ".join(words[:max_words]) + "..." if len(words) > max_words else text

# ממיר מחרוזת של תאריך לפורמט datetime
def parse_date_string(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.now()