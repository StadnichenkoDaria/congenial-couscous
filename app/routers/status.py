from fastapi import APIRouter, status

from app.database.engine import check_availability
from app.models.app_status import AppStatus

router = APIRouter()


@router.get("/status", status_code=status.HTTP_200_OK)
def get_status() -> AppStatus:
    return AppStatus(database=check_availability())
