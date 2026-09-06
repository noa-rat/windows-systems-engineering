from pydantic import BaseModel, Field, RootModel


class CredentialsRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class UserResponse(BaseModel):
    id: int
    username: str


class CurrentUser(UserResponse):
    pass


class LoginResponse(BaseModel):
    success: bool
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    success: bool


class ArticleResponse(BaseModel):
    title: str
    summary: str
    fulltext: str
    category: str | None = None
    date: str


class ChatArticle(BaseModel):
    title: str = Field(default="", max_length=500)
    summary: str = Field(default="", max_length=8000)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)
    article: ChatArticle | None = None


class ChatResponse(BaseModel):
    answer: str


class PreferencesRequest(BaseModel):
    user_id: int
    favorite_categories: list[str] = Field(default_factory=lambda: ["general"], max_length=10)
    dark_mode: bool = False


class PreferencesResponse(BaseModel):
    favorite_categories: list[str]
    dark_mode: bool


class PreferencesUpdateResponse(BaseModel):
    success: bool


class GraphResponse(RootModel[dict[str, int]]):
    pass


class NewsApiArticle(BaseModel):
    title: str = ""
    description: str | None = None
    content: str | None = None
    publishedAt: str = ""
