from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    user_id: int
    dark_mode: bool = False
    favorite_categories: list[str] = Field(default_factory=lambda: ["general"])