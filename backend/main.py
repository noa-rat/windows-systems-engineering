# backend/main.py
# run: uvicorn backend.main:app --reload
# מפעיל את השרת

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.controllers import news_controller, user_controller, chat_controller, graph_controller

# יצירת מופע של השרת
app = FastAPI(title="AI News API")

# הגדרת הרשאות גישה
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# רישום של הנתבים השונים (כל ה-controller-ים)
app.include_router(user_controller.router)
app.include_router(news_controller.router)
app.include_router(chat_controller.router)
app.include_router(graph_controller.router)

# דף ראשי
@app.get("/")
async def root():
    return {"message": "Welcome to AI NEWS API"}