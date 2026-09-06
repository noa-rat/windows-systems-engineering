from backend.database import get_connection
from backend.passwords import hash_password, verify_password
from backend.models.api_models import UserResponse
from backend.models.preferences_model import UserPreferences
import json

def verify_user_exists(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Username, Password
        FROM Users 
        WHERE Username = ?
    """, (username,))

    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return None

    stored_password = str(row[2])
    valid_password = verify_password(password, stored_password)

    if not valid_password and stored_password == password:
        valid_password = True
        cursor.execute(
            "UPDATE Users SET Password = ? WHERE Id = ?",
            (hash_password(password), row[0])
        )
        conn.commit()

    cursor.close()
    conn.close()

    if not valid_password:
        return None

    return UserResponse(id=row[0], username=row[1])

def get_user_preferences(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT FavoriteCategories, DarkMode FROM UserPreferences WHERE UserID = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return UserPreferences(
            user_id=user_id,
            favorite_categories=json.loads(row[0]),
            dark_mode=bool(row[1]),
        )
    return UserPreferences(user_id=user_id)