from fastapi import APIRouter
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.admin import Admin
from starlette import status

admin_router = APIRouter()

@admin_router.post(
    path="/api/login",
    tags=["Auth"]
)
def login(admin: Admin):
    if admin.email == "admin@gmail.com" and admin.password == "admin":
        token : str = create_token(admin.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})