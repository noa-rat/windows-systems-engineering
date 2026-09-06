from backend.gateway.newsapi_gateway import fetch_from_newsapi
from backend.gateway.ollama_gateway import summarize_with_ollama
from backend.database import get_connection

def fetch_and_store_news_if_needed(category):
    articles = fetch_from_newsapi(category)

    conn = get_connection()
    cursor = conn.cursor()
    added_count = 0

    try:
        for article in articles:
            title = article.title.strip()
            content = article.content or article.description or ""
            published = article.publishedAt
            if not title:
                continue
            summary = summarize_with_ollama(content)

            cursor.execute(
                "SELECT COUNT(*) FROM NewsSummaries WHERE Title = ? AND Date = ?",
                (title, published),
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO NewsSummaries (Title, FullText, Summary, Category, Date)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, content, summary, category, published))
                added_count += 1
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
    return added_count