from backend.database import get_connection
from backend.models.news_model import NewsItem


def _news_items(rows):
    return [
        NewsItem(
            title=row[0],
            summary=row[1] or "",
            fulltext=row[2] or "",
            category=row[3] or "",
            date=row[4].strftime("%Y-%m-%d"),
        )
        for row in rows
    ]


def get_news_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Title, Summary, FullText, Category, Date
            FROM NewsSummaries
            WHERE Category = ?
            ORDER BY Date DESC
        """, (category,))
        return _news_items(cursor.fetchall())
    finally:
        cursor.close()
        conn.close()


def search_news_by_keyword(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        keyword_like = f"%{keyword}%"
        cursor.execute("""
            SELECT Title, Summary, FullText, Category, Date
            FROM NewsSummaries
            WHERE Title LIKE ? OR Summary LIKE ?
            ORDER BY Date DESC
        """, (keyword_like, keyword_like))
        return _news_items(cursor.fetchall())
    finally:
        cursor.close()
        conn.close()


def get_news_statistics_by_category():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Category, COUNT(*)
            FROM NewsSummaries
            GROUP BY Category
        """)
        return {str(row[0]): int(row[1]) for row in cursor.fetchall()}
    finally:
        cursor.close()
        conn.close()
