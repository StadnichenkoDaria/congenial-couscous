from fastapi import APIRouter, status

from app.database import users_db
from app.models.app_status import AppStatus

router = APIRouter()


@router.get("/status", status_code=status.HTTP_200_OK)
def get_status() -> AppStatus:
    return AppStatus(users=bool(users_db))
