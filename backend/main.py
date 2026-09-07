# uvicorn backend.main:app --reload

import pyodbc
import requests
from collections import defaultdict, deque
from time import monotonic
from threading import Lock
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.controllers import news_controller, user_controller, chat_controller, graph_controller

app = FastAPI(title="AI News API")

_rate_limit_lock = Lock()
_rate_limit_events = defaultdict(deque)
_RATE_LIMIT_WINDOW = 60
_RATE_LIMIT_REQUESTS = 120
_MAX_REQUEST_BYTES = 1_000_000


@app.middleware("http")
async def request_guardrails(request: Request, call_next):
    if settings.FORCE_HTTPS and request.url.scheme != "https":
        secure_url = request.url.replace(scheme="https")
        return JSONResponse(
            status_code=307,
            headers={"Location": str(secure_url)},
            content={"detail": "HTTPS is required."},
        )

    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > _MAX_REQUEST_BYTES:
        return JSONResponse(status_code=413, content={"detail": "Request is too large."})

    client_id = request.client.host if request.client else "unknown"
    now = monotonic()
    with _rate_limit_lock:
        events = _rate_limit_events[client_id]
        while events and now - events[0] > _RATE_LIMIT_WINDOW:
            events.popleft()
        if len(events) >= _RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
            )
        events.append(now)

    return await call_next(request)


@app.exception_handler(requests.RequestException)
async def external_service_error(_: Request, exc: requests.RequestException):
    return JSONResponse(
        status_code=503,
        content={"detail": f"External service unavailable: {exc}"},
    )


@app.exception_handler(pyodbc.Error)
async def database_error(_: Request, __: pyodbc.Error):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database service is temporarily unavailable."},
    )


@app.exception_handler(RuntimeError)
async def service_runtime_error(_: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


@app.exception_handler(TimeoutError)
async def timeout_error(_: Request, exc: TimeoutError):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.ALLOWED_ORIGINS.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(user_controller.router)
app.include_router(news_controller.router)
app.include_router(chat_controller.router)
app.include_router(graph_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI NEWS API"}