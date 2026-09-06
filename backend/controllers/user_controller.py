# backend/controllers/user_controller.py
# מנהל משתמשים: הרשמה, התחברות וניהול העדפות משתמש

from fastapi import APIRouter, HTTPException, Request
from backend.queries.user_queries import verify_user_exists
from backend.commands.user_commands import create_new_user, update_user_preferences
from backend.queries.user_queries import get_user_preferences
import json

# נתיב בסיס לניהול משתמשים
router = APIRouter(prefix="/auth", tags=["Authentication"])

# התחברות
@router.post("/login")
def login_user(data: dict):
    print("📥 LOGIN ATTEMPT:", data)
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    # מאמת פרטי משתמש במסד הנתונים
    user = verify_user_exists(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"success": True, "user": user}

# הרשמה
@router.post("/register")
def register_user(data: dict):
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing data")

    # בודק שלא קיים משתמש זהה ומוסיף משתמש חדש
    created = create_new_user(username, password)
    if not created:
        raise HTTPException(status_code=409, detail="User already exists")

    return {"success": True}

# קבלת העדפות משתמש
@router.get("/preferences")
def get_preferences(user_id: int):
    return get_user_preferences(user_id)

# עדכון העדפות משתמש
@router.post("/preferences")
def update_preferences(prefs: dict):
    user_id = prefs.get("user_id")
    return update_user_preferences(user_id, prefs)