# backend/controllers/chat_controller.py
# מנהל את התקשורת עם ollam כולל מימוש RAG

from fastapi import APIRouter
from backend.database import get_connection
from backend.gateway.ollama_gateway import ask_ollama
import re

# נתיב לתקשורת עם ollama
router = APIRouter(prefix="/ask-ai", tags=["AI Agent"])

@router.post("/")
def ask_ai(data: dict):
    # שאלה
    prompt = data.get("prompt", "")
    if not prompt:
        return {"answer": "Prompt is empty"}

    # כתבה נבחרת
    article = data.get("article")

    if article:
        # הוספת הקשר מהכתבה הנבחרת
        title = article.get("title", "")
        summary = article.get("summary", "")
        context = f"{title}\n\n{summary}"
    else:
        # הוספת הקשר מתוך מסד הנתונים (RAG)
        context = retrieve_context(prompt)

    if context:
        full_prompt = f"""Context:
        {context}
    
        Question:
        {prompt}
        """

        # תשובה
        response = ask_ollama(full_prompt)
        print(f"שולח שאלה עם הקשר ל-ollama:\n{full_prompt}")
    else:
        response = ask_ollama(prompt)
        print(f"שולח שאלה ללא הקשר ל-ollama:\n{prompt}")

    return {"answer": response}

# מחלץ מילות מפתח מתוך השאלה
def extract_keywords(prompt):
    # מילים לא רלוונטיות
    stopwords = {
        "what", "who", "when", "why", "how", "is", "are", "was", "were", "the", "a", "an",
        "of", "in", "on", "at", "by", "for", "with", "without", "this", "that",
        "there", "it", "and", "or", "but", "if", "not", "yes", "no", "do", "does", "did",
        "can", "could", "should", "would", "will", "i", "you", "he", "she", "they", "we", "to",
        "be", "has", "have", "had"
    }
    words = re.findall(r"\w+", prompt.lower())
    # רשימת מילות המפתח
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    return keywords

# מחזיר עד 3 כתבות רלוונטיות לפי מילות המפתח
def retrieve_context(prompt):
    keywords = extract_keywords(prompt)
    if not keywords:
        return None

    # מחפש תקציר או כותרת שמכילים מילת מפתח
    placeholders = " OR ".join(["Summary LIKE ? OR Title LIKE ?" for _ in keywords])
    values = sum([[f"%{word}%", f"%{word}%"] for word in keywords], [])

    # שולח שאילתא למסד הנתונים
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT TOP 3 Summary FROM NewsSummaries
        WHERE {placeholders}
        ORDER BY Date DESC
    """, values)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    # מחזיר את רשימת התוצאות
    return "\n\n".join([r[0] for r in results]) if results else None