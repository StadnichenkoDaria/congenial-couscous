import json

import uvicorn
from fastapi_pagination import Page, add_pagination, paginate, Params
from fastapi import FastAPI, status, HTTPException, Query
from models.app_status import AppStatus
from models.login import Login
from models.user import User
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


@app.get('/api/users', response_model=Page[User])
def get_users():
    return paginate(users)


@app.get("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.post("/api/login", status_code=status.HTTP_201_CREATED)
def login(credentials: Login) -> dict:
    valid_login = "eve.holt@reqres.in"
    valid_password = "cityslicka"
    token = "QpwL5tke4Pnpja7X4"

    if credentials.email == valid_login and credentials.password == valid_password:
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if user.id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID should not be provided when creating a user"
        )

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
        users_dict = [u.model_dump(mode='json') for u in users]
        json.dump(users_dict, f, indent=2)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "avatar": str(new_user.avatar),
        "createdAt": created_at
    }


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

    with open("../users.json", "w") as f:
        users_dict = [u.model_dump(mode='json') for u in users]
        json.dump(users_dict, f, indent=2)

    return None


if __name__ == "__main__":
    try:
        with open("../users.json") as f:
            users = [User.model_validate(user) for user in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
        print("Starting with empty users list")
    except Exception as e:
        users = []
        print(f"Error loading users: {e}")

    print(f"Loaded {len(users)} users")
    uvicorn.run(app, host="0.0.0.0", port=8000)
