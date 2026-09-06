from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio

from backend.config import settings


_executor = ThreadPoolExecutor(
    max_workers=settings.SERVER_MAX_WORKERS,
    thread_name_prefix="backend-worker",
)


async def run_blocking(function, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _executor,
        partial(function, *args, **kwargs),
    )
