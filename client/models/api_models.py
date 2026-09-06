from pydantic import BaseModel, Field


class MappingModel(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def items(self):
        return self.model_dump().items()


class ClientUser(MappingModel):
    id: int
    username: str


class LoginResult(MappingModel):
    success: bool
    user: ClientUser | None = None
    access_token: str | None = None
    token_type: str = "bearer"
    detail: str | None = None


class RegisterResult(MappingModel):
    success: bool
    detail: str | None = None


class ArticleResult(MappingModel):
    title: str
    summary: str
    fulltext: str
    category: str | None = None
    date: str


class PreferencesResult(MappingModel):
    favorite_categories: list[str] = Field(default_factory=lambda: ["general"])
    dark_mode: bool = False


class GraphResult(MappingModel):
    values: dict[str, int] = Field(default_factory=dict)

    def items(self):
        return self.values.items()
