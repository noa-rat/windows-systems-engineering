from fastapi import APIRouter, Depends
from backend.queries.news_queries import get_news_statistics_by_category
from backend.security import get_current_user
from backend.models.api_models import CurrentUser, GraphResponse
from backend.runtime import run_blocking

router = APIRouter(prefix="/graphs", tags=["Graphs"])


@router.get("/by-category", response_model=GraphResponse)
async def graph_by_category(_: CurrentUser = Depends(get_current_user)):
    statistics = await run_blocking(get_news_statistics_by_category)
    return GraphResponse(statistics)