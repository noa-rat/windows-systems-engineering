# backend/commands/user_commands.py
# מנהל עדכון נתוני משתמשים

import json
from backend.database import get_connection

# רישום משתמש
def create_new_user(username, password):
    try:
        # חיבור למסד הנתונים
        conn = get_connection()
        cursor = conn.cursor()

        # בדיקה אם המשתמש כבר קיים
        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            return False

        # הוספת משתמש חדש
        cursor.execute("""
            INSERT INTO Users (Username, Password)
            VALUES (?, ?)
        """, (username, password))
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("שגיאה ביצירת משתמש:", e)
        return False

# עדכון העדפות משתמש
def update_user_preferences(user_id: int, prefs: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # מחלץ את ההעדפות מתוך הפרמטרים
    fav = json.dumps(prefs.get("favorite_categories", ["general"]))
    dark = int(prefs.get("dark_mode", False))

    # אם קיימת שורה עבור המשתמש - מתבצע עדכון
    # אחרת - מתבצעת הוספת שורה עבורו
    cursor.execute("""
        IF EXISTS (SELECT 1 FROM UserPreferences WHERE UserID = ?)
        BEGIN
            UPDATE UserPreferences SET FavoriteCategories=?, DarkMode=? WHERE UserID=?
        END
        ELSE
        BEGIN
            INSERT INTO UserPreferences (UserID, FavoriteCategories, DarkMode) VALUES (?, ?, ?)
        END
    """, (user_id, fav, dark, user_id, user_id, fav, dark))

    conn.commit()
    conn.close()
    return {"success": True}