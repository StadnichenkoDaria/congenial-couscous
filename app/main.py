import dotenv

dotenv.load_dotenv()

import uvicorn
from fastapi_pagination import add_pagination
from fastapi import FastAPI
from routers import status, users, root, login
from app.database.engine import create_db_and_tables

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
app.include_router(root.router)
app.include_router(login.router)
add_pagination(app)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
