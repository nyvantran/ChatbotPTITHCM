from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.storage.mongodb import mongo_storage

from app.api.v1.deps import get_current_user

router = APIRouter()
# db = mongo_storage.get_db()
service = UserService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    return service.register_user(user_in)


@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    return service.authenticate_user(user_in)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return {"message": f"User {current_user['email']} đã đăng xuất thành công"}
