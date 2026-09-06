from datetime import datetime

def truncate_text(text, max_words=60):
    words = text.split()
    return " ".join(words[:max_words]) + "..." if len(words) > max_words else text

def parse_date_string(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.now()