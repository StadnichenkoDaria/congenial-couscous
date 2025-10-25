import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import Params, paginate

from app.database import users_db
from app.models.user import User

router = APIRouter(prefix="/api/users")


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(
        page: Optional[int] = Query(None, ge=1),
        size: Optional[int] = Query(None, ge=1)
):
    if page is None and size is None:
        params = Params(page=1, size=len(users_db))
        return paginate(users_db, params)

    if page is not None and size is None:
        params = Params(page=page, size=6)
        return paginate(users_db, params)

    params = Params(page=page or 1, size=size or 6)
    return paginate(users_db, params)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    new_id = max((u.id for u in users), default=0) + 1
    created_at = datetime.now().isoformat() + "Z"

    new_user = User(
        id=new_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=user.avatar
    )
    users.append(new_user)

    with open("../users.json", "w") as f:
        users_dict = [u.model_dump(mode='json') for u in users]  # mode='json' конвертирует HttpUrl автоматически
        json.dump(users_dict, f, indent=2)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "avatar": str(new_user.avatar),
        "createdAt": created_at
    }


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    users[user_id - 1] = user
    return user


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def partial_update_user(user_id: int, user: User) -> User:
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing_user = users[user_id - 1]
    if user.name:
        existing_user.name = user.name
    if user.email:
        existing_user.email = user.email

    return existing_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    users.pop(user_id - 1)

    with open("../users.json", "w") as f:
        users_dict = [u.model_dump(mode='json') for u in users]
        json.dump(users_dict, f, indent=2)

    return None
