# backend/database.py
# פתיחת חיבור למסד הנתונים

import pyodbc
from backend.config import settings

def get_connection():
    try:
        conn = pyodbc.connect(settings.DATABASE_URL)
        return conn
    except Exception as e:
        print("❌ שגיאה בחיבור למסד הנתונים:", e)
        return None