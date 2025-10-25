from fastapi import APIRouter, status, HTTPException
from app.models.login import Login

router = APIRouter()


@router.post("/api/login", status_code=status.HTTP_200_OK)
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
