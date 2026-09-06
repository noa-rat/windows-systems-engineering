# backend/config.py
# הגדרות עבור חיבורים חיצוניים

from pydantic_settings import BaseSettings
import pyodbc

class Settings(BaseSettings):
    # מפתח API ל-NewsAPI
    NEWS_API_KEY: str = "5c567455b0f840eba81710a63a0fe79a"
    # פרטי התחברות למסד הנתונים
    DATABASE_URL: str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "Server=noaRattDB.mssql.somee.com;"
        "Database=noaRattDB;"
        "Uid=noa-ratt_SQLLogin_1;"
        "Pwd=gp12a9juxe;"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
    )

    # שם מודל ה-ollama
    OLLAMA_MODEL: str = "tinyllama"

settings = Settings()


def test_connection():
    print("מנסה להתחבר למסד הנתונים...")
    try:
        # פתיחת חיבור עם הגבלת זמן כדי שלא ייתקע לנצח
        conn = pyodbc.connect(settings.DATABASE_URL, timeout=10)
        print("✅ החיבור למסד הנתונים עובד בהצלחה!")

        # בדיקה נוספת: שליפת גרסת השרת כדי לוודא שניתן להריץ שאילתות
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print(f"גרסת השרת: {row[0]}")

        conn.close()
    except pyodbc.Error as ex:
        print("❌ שגיאה בחיבור למסד הנתונים:")
        sqlstate = ex.args[0]
        print(f"קוד מצב (SQL State): {sqlstate}")
        # במקרה של שגיאת ODBC, האיבר השני מכיל את הודעת השגיאה המפורטת
        if len(ex.args) > 1:
            print(f"פרטי השגיאה: {ex.args[1]}")
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")


if __name__ == "__main__":
    test_connection()