from threading import Lock

import numpy as np

from backend.database import get_connection
from backend.gateway.ollama_client import embed


TOP_K = 3
MIN_SIMILARITY = 0.25

_index_lock = Lock()
_documents = []
_embeddings = np.empty((0, 0), dtype=np.float32)
_indexed_signature = None


def _load_documents():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT Id, Title, Summary, Date
            FROM NewsSummaries
            WHERE Summary IS NOT NULL
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def _refresh_index():
    global _documents, _embeddings, _indexed_signature

    rows = _load_documents()
    signature = tuple((row[0], row[1], row[2], row[3]) for row in rows)
    with _index_lock:
        if signature == _indexed_signature:
            return

    documents = [
        {
            "id": row[0],
            "title": row[1] or "",
            "summary": row[2] or "",
        }
        for row in rows
    ]
    texts = [f"{item['title']}\n{item['summary']}" for item in documents]
    vectors = embed(texts) if texts else []
    embeddings = np.asarray(vectors, dtype=np.float32)
    if embeddings.size:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / np.maximum(norms, 1e-12)

    with _index_lock:
        _documents = documents
        _embeddings = embeddings
        _indexed_signature = signature


def search_similar_articles(prompt: str, top_k: int = TOP_K) -> list[str]:
    _refresh_index()
    with _index_lock:
        if not _documents:
            return []

        documents = list(_documents)
        embeddings = _embeddings.copy()

    query_embedding = np.asarray(embed([prompt])[0], dtype=np.float32)
    query_embedding /= max(float(np.linalg.norm(query_embedding)), 1e-12)
    similarities = embeddings @ query_embedding
    ranked_indexes = np.argsort(similarities)[::-1]

    return [
        documents[index]["summary"]
        for index in ranked_indexes[:top_k]
        if similarities[index] >= MIN_SIMILARITY
    ]
