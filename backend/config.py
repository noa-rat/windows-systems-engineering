import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class Settings(BaseSettings):
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    SOMEE_DB_PASSWORD: str = os.getenv("SOMEE_DB_PASSWORD", "")
    DATABASE_URL: str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=noaRattDB.mssql.somee.com;"
        "DATABASE=noaRattDB;"
        "UID=noa-ratt_SQLLogin_1;"
        f"PWD={os.getenv('SOMEE_DB_PASSWORD', '')};"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
    )
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_GENERATION_MODEL: str = os.getenv("OLLAMA_GENERATION_MODEL", "tinyllama")
    OLLAMA_EMBEDDING_MODEL: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    OLLAMA_GENERATION_TIMEOUT: int = 120
    OLLAMA_EMBEDDING_TIMEOUT: int = 120
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_EXPIRE_MINUTES: int = 60
    DB_POOL_MIN_SIZE: int = 2
    DB_POOL_MAX_SIZE: int = 10
    SERVER_MAX_WORKERS: int = 8
    NEWS_API_TIMEOUT: int = 20
    NEWS_MAX_ARTICLES: int = 20
    CHAT_MAX_PROMPT_LENGTH: int = 4000
    CHAT_MAX_CONTEXT_LENGTH: int = 12000
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000")
    FORCE_HTTPS: bool = os.getenv("FORCE_HTTPS", "false").lower() == "true"


settings = Settings()

if not settings.JWT_SECRET:
    raise RuntimeError("JWT_SECRET must be configured in .env.")
if len(settings.JWT_SECRET) < 32:
    raise RuntimeError("JWT_SECRET must contain at least 32 characters.")
if not settings.SOMEE_DB_PASSWORD:
    raise RuntimeError("SOMEE_DB_PASSWORD must be configured in .env.")
if not settings.NEWS_API_KEY:
    raise RuntimeError("NEWS_API_KEY must be configured in .env.")
