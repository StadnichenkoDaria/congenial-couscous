from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page, paginate

from app.database import users
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")


@router.get("/", status_code=status.HTTP_200_OK, response_model=Page[User])
def get_users() -> Page[User]:
    return paginate(users.get_users())


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid user")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid user")
    users.delete_user(user_id)
    return {"message": "User deleted"}
