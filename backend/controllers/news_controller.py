from fastapi import APIRouter, Depends, Query
from backend.queries.news_queries import get_news_by_category, search_news_by_keyword
from backend.commands.news_commands import fetch_and_store_news_if_needed
from backend.security import get_current_user
from backend.models.api_models import ArticleResponse, CurrentUser
from backend.runtime import run_blocking

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/", response_model=list[ArticleResponse])
async def get_news(category: str = Query("general"), _: CurrentUser = Depends(get_current_user)):
    return await run_blocking(get_news_by_category, category)


@router.post("/refresh", response_model=list[ArticleResponse])
async def refresh_news(category: str = Query("general"), _: CurrentUser = Depends(get_current_user)):
    await run_blocking(fetch_and_store_news_if_needed, category)
    return await run_blocking(get_news_by_category, category)


@router.get("/search", response_model=list[ArticleResponse])
async def search_news(q: str = Query(..., min_length=1, max_length=200), _: CurrentUser = Depends(get_current_user)):
    return await run_blocking(search_news_by_keyword, q)