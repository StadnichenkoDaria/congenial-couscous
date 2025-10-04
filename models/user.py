from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, Field


class User(BaseModel):
    id: Optional[int] = None
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
