import json
import pyodbc
from backend.database import get_connection
from backend.passwords import hash_password
from backend.models.preferences_model import UserPreferences
from backend.models.api_models import PreferencesUpdateResponse

def create_new_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            return False

        cursor.execute("""
            INSERT INTO Users (Username, Password)
            VALUES (?, ?)
        """, (username, hash_password(password)))
        conn.commit()
        return True

    except pyodbc.IntegrityError:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_user_preferences(prefs: UserPreferences):
    conn = get_connection()
    cursor = conn.cursor()

    fav = json.dumps(prefs.favorite_categories)
    dark = int(prefs.dark_mode)
    user_id = prefs.user_id

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
    return PreferencesUpdateResponse(success=True)