from fastapi.responses import JSONResponse
from app.data import users_db, example_support
from app.models import ResponseModel, UserCreate, LoginRequest, UsersResponse, UserCreateResponse, UserUpdateResponse, \
    UserUpdate
from fastapi import FastAPI, status, HTTPException
from datetime import datetime
import uuid

app = FastAPI()


@app.get("/api/users", response_model=UsersResponse)
def get_users(page: int = 1, per_page: int = 6):
    total_users = len(users_db)
    total_pages = (total_users + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    start = (page - 1) * per_page
    end = start + per_page
    users_list = list(users_db.values())[start:end]

    return UsersResponse(
        page=page,
        per_page=per_page,
        total=total_users,
        total_pages=total_pages,
        data=users_list,
        support=example_support
    )


@app.get("/api/users/{user_id}", response_model=ResponseModel)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    return ResponseModel(data=user, support=example_support)


@app.post("/api/login")
def login(login_request: LoginRequest):
    valid_login = "eve.holt@reqres.in"
    valid_password = "cityslicka"
    token = "QpwL5tke4Pnpja7X4"
    if not login_request.password:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "Missing password"})

    if login_request.email == valid_login and login_request.password == valid_password:
        access_token = token
        return {"token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


@app.post("/api/users", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_id = str(uuid.uuid4().int)[:6]
    new_user = {
        "name": user.name,
        "job": user.job,
        "id": new_id,
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    return UserCreateResponse(**new_user)


@app.put("/api/users/{user_id}", response_model=UserUpdateResponse)
def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    current_user = users_db[user_id]
    current_user.name = user.name
    current_user.job = user.job

    updated_at = datetime.utcnow().isoformat() + "Z"

    return UserUpdateResponse(
        name=user.name,
        job=user.job,
        updatedAt=updated_at
    )


@app.patch("/api/users/{user_id}", response_model=UserUpdateResponse)
def patch_update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    current_user = users_db[user_id]
    current_user.name = user.name
    current_user.job = user.job

    updated_at = datetime.utcnow().isoformat() + "Z"

    return UserUpdateResponse(
        name=user.name,
        job=user.job,
        updatedAt=updated_at
    )


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del users_db[user_id]
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
