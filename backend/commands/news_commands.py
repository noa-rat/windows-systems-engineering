# backend/commands/news_commands.py
# מנהל את ייבוא הכתבות, עיבודן ושמירתן
# מנהל אינטגרציה עם NewsAPI, ollama ומסד הנתונים ב-somee.com

from backend.gateway.newsapi_gateway import fetch_from_newsapi
from backend.gateway.ollama_gateway import summarize_with_ollama
from backend.database import get_connection

# מייבא כתבות לפי קטגוריה, מסכם ושומר
def fetch_and_store_news_if_needed(category):
    # ייבוא
    articles = fetch_from_newsapi(category)

    conn = get_connection()
    cursor = conn.cursor()
    added_count = 0

    for article in articles:
        # סיכום
        title = article.get("title", "").strip()
        content = article.get("content") or article.get("description") or ""
        published = article.get("publishedAt", "")
        summary = summarize_with_ollama(content)

        # שמירה
        cursor.execute("SELECT COUNT(*) FROM NewsSummaries WHERE Title = ? AND Date = ?", (title, published))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO NewsSummaries (Title, FullText, Summary, Category, Date)
                VALUES (?, ?, ?, ?, ?)
            """, (title, content, summary, category, published))
            conn.commit()
            added_count += 1
    print(f"✅ Total added {added_count} new articles.")

    cursor.close()
    conn.close()