from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    id: int | None = None
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UsersResponse(BaseModel):
    items: list[User]
    total: int
    page: int
    size: int
    pages: int
