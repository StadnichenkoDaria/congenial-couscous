import json
import uvicorn
from fastapi_pagination import add_pagination
from fastapi import FastAPI

from app.models.user import User
from routers import status, users, root, login
from database import users_db

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
app.include_router(root.router)
app.include_router(login.router)
add_pagination(app)


if __name__ == "__main__":
    try:
        with open("../users.json") as f:
            users_db.extend([User.model_validate(user) for user in json.load(f)])
    except (FileNotFoundError, json.JSONDecodeError):
        users_db = []
        print("Starting with empty users list")
    except Exception as e:
        users_db = []
        print(f"Error loading users: {e}")

    print(f"Loaded {len(users_db)} users")
    uvicorn.run(app, host="0.0.0.0", port=8000)
