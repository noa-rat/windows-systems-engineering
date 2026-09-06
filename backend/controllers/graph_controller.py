# backend/controllers/graph_controller.py
# מספק נתונים ליצירת גרפים

from fastapi import APIRouter
from backend.queries.news_queries import get_news_statistics_by_category

# נתיב בסיס לניהול הגרפים
router = APIRouter(prefix="/graphs", tags=["Graphs"])

# מספר הכתבות לפי קטגוריה
@router.get("/by-category")
def graph_by_category():
    return get_news_statistics_by_category()