# backend/controllers/news_controller.py
# מנהל שליפת כתבות ושמירתן במסד הנתונים

from fastapi import APIRouter, Query
from backend.queries.news_queries import get_news_by_category, search_news_by_keyword
from backend.commands.news_commands import fetch_and_store_news_if_needed

# נתיב בסיס לשליפת כתבות
router = APIRouter(prefix="/news", tags=["News"])

# שולף כתבות לפי קטגוריה
@router.get("/")
def get_news(category: str = Query("general")):
    # שולפת כתבות חדשות רק אם אין מספיק כתבות קיימות בקטגוריה
    fetch_and_store_news_if_needed(category)
    # מחזירה כתבות ממסד הנתונים לפי הקטגוריה
    return get_news_by_category(category)

# שולף כתבות לפי מילות מפתח
@router.get("/search")
def search_news(q: str = Query(...)):
    return search_news_by_keyword(q)