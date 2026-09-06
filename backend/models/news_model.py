from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    fulltext: str
    summary: str
    category: str
    date: str