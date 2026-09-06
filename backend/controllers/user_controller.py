from fastapi import APIRouter, Depends, HTTPException
from backend.queries.user_queries import verify_user_exists
from backend.commands.user_commands import create_new_user, update_user_preferences
from backend.queries.user_queries import get_user_preferences
from backend.security import create_access_token, get_current_user
from backend.runtime import run_blocking
from backend.models.api_models import (
    CredentialsRequest,
    CurrentUser,
    LoginResponse,
    PreferencesRequest,
    PreferencesResponse,
    PreferencesUpdateResponse,
    RegisterResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login_user(data: CredentialsRequest):
    username = data.username
    password = data.password

    user = await run_blocking(verify_user_exists, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return LoginResponse(
        success=True,
        user=user,
        access_token=create_access_token(user),
    )

@router.post("/register", response_model=RegisterResponse)
async def register_user(data: CredentialsRequest):
    username = data.username
    password = data.password

    created = await run_blocking(create_new_user, username, password)
    if not created:
        raise HTTPException(status_code=409, detail="User already exists")

    return RegisterResponse(success=True)

@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(user_id: int, current_user: CurrentUser = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return await run_blocking(get_user_preferences, user_id)

@router.post("/preferences", response_model=PreferencesUpdateResponse)
async def update_preferences(
    prefs: PreferencesRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    user_id = prefs.user_id
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return await run_blocking(update_user_preferences, prefs)