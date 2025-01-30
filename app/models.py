from pydantic import BaseModel
from typing import Dict, List, Optional, Union


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str
    name: Optional[str] = None
    job: Optional[str] = None


class UserCreate(BaseModel):
    name: str
    job: str


class UserCreateResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str


class UserUpdate(BaseModel):
    name: str
    job: str


class UserUpdateResponse(BaseModel):
    name: str
    job: str
    updatedAt: str


class Support(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: User
    support: Support


class ResponseCreateUserModel(BaseModel):
    data: Dict[str, Union[str, int]]


class UsersResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[User]
    support: Support


class LoginRequest(BaseModel):
    email: str
    password: str
