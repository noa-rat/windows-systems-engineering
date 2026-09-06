# backend/queries/user_queries.py
# מנהל את שליפת הנתונים עבור המשתמשים מתוך מסד הנתונים

from backend.database import get_connection
import json

# אימות שם משתמש וסיסמה
def verify_user_exists(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Username
        FROM Users 
        WHERE Username = ? AND Password = ?
    """, (username, password))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
        }
    return None

# מחזיר את העדפות המשתמש
def get_user_preferences(user_id: int):
    # מתקשר עם מסד הנתונים
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT FavoriteCategories, DarkMode FROM UserPreferences WHERE UserID = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    # ממיר לטיפוס מילון
    if row:
        return {
            "favorite_categories": json.loads(row[0]),
            "dark_mode": bool(row[1])
        }
    # אם לא קיים - מחזיר את ערכי ברירת המחדל
    return {
        "favorite_categories": ["general"],
        "dark_mode": False
    }