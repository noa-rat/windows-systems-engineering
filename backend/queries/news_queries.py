# backend/queries/news_queries.py
# מנהל את שליפת הכתבות מתוך מסד הנתונים

from backend.database import get_connection

# מחזירה רשימת כתבות לפי קטגוריה
def get_news_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()

    # מריצה את השאילתא
    cursor.execute("""
                   SELECT Title, Summary, FullText, Date
                   FROM NewsSummaries
                   WHERE Category = ?
                   ORDER BY Date DESC
                   """, (category,))

    # קולטת את רשימת התוצאות
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # ממירה לטיפוס מילון
    return [
        {
            "title": row[0],
            "summary": row[1],
            "fulltext": row[2],
            "date": row[3].strftime("%Y-%m-%d")
        }
        for row in rows
    ]

# מחזירה רשימת כתבות לפי מילות מפתח
def search_news_by_keyword(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    # מחפשת כתבות עם אחת ממילות המפתח בכותרת או בתקציר
    keyword_like = f"%{keyword}%"
    cursor.execute("""
                   SELECT Title, Summary, FullText, Date
                   FROM NewsSummaries
                   WHERE Title LIKE ? OR Summary LIKE ?
                   ORDER BY Date DESC
                   """, (keyword_like, keyword_like))

    # קולטת את רשימת התוצאות
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # ממירה לטיפוס מילון
    return [
        {
            "title": row[0],
            "summary": row[1],
            "fulltext": row[2],
            "date": row[3].strftime("%Y-%m-%d")
        }
        for row in rows
    ]

# מחזירה את מספר הכתבות בכל קטגוריה
def get_news_statistics_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    # מריצה את השאילתא לספירה לפי קטגוריה
    cursor.execute("""
                   SELECT Category, COUNT(*)
                   FROM NewsSummaries
                   GROUP BY Category
                   """)
    # קולטת את התוצאות וממירה לטיפוס מילון
    data = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    conn.close()
    return data