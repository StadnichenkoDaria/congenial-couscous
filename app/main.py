import json
from typing import Optional

import uvicorn
from fastapi_pagination import add_pagination, paginate, Params
from fastapi import FastAPI, status, HTTPException, Query
from models.app_status import AppStatus
from models.login import Login
from models.user import User, CreateUser
from datetime import datetime

app = FastAPI()
add_pagination(app)

users: list[User] = []


@app.get("/")
def read_root():
    return {"message": "hello"}


@app.get("/status", status_code=status.HTTP_200_OK)
def get_status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get('/api/users', status_code=status.HTTP_200_OK)
def get_users(
        page: Optional[int] = Query(None, ge=1),
        size: Optional[int] = Query(None, ge=1)
):
    if page is None and size is None:
        params = Params(page=1, size=len(users))
        return paginate(users, params)

    if page is not None and size is None:
        params = Params(page=page, size=6)
        return paginate(users, params)

    params = Params(page=page or 1, size=size or 6)
    return paginate(users, params)


@app.get("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.post("/api/login", status_code=status.HTTP_200_OK)
def login(credentials: Login) -> dict:
    valid_login = "eve.holt@reqres.in"
    valid_password = "cityslicka"
    token = "QpwL5tke4Pnpja7X4"
    if not credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if credentials.email == valid_login and credentials.password == valid_password:
        access_token = token
        return {"token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser):
    new_id = str(len(users) + 1)
    created_at = datetime.now().isoformat() + "Z"

    new_user = {**user.dict(), "id": new_id, "createdAt": created_at}
    users.append(new_user)

    with open("../users.json", "w") as f:
        json.dump(users, f)

    return new_user


@app.put("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    users[user_id - 1] = user
    return user


@app.patch("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def partial_update_user(user_id: int, user: User) -> User:
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing_user = users[user_id - 1]
    if user.name:
        existing_user.name = user.name
    if user.email:
        existing_user.email = user.email

    return existing_user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    users.pop(user_id - 1)
    return None


if __name__ == "__main__":
    with open("../users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("Users loaded")
    uvicorn.run(app, host="0.0.0.0", port=8000)
