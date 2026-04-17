from fastapi import HTTPException, status
from pymongo.database import Database
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from app.storage.mongodb import mongo_storage
from loguru import logger
from bson import ObjectId


class UserService:
    db = mongo_storage.get_db()
    collection = db["users"]

    # def __init__(self, db: Database):
    def get_user_by_id(self, user_id: str):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def register_user(self, user_in: UserCreate):
        """đăng ký người dùng mới"""
        if user_in.password != user_in.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu xác nhận không khớp"
            )

        # Check existing user
        existing_user = self.collection.find_one({"email": user_in.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã được đăng ký"
            )

        user_data = {
            "email": user_in.email,
            "hashed_password": get_password_hash(user_in.password),
            "is_active": True
        }

        result = self.collection.insert_one(user_data)
        logger.info(f"User registered: {user_in.email}")
        return {**user_data, "id": str(result.inserted_id)}

    def authenticate_user(self, user_in: UserLogin):
        """đăng nhập người dùng """
        user = self.collection.find_one({"email": user_in.email})
        if not user or not verify_password(user_in.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không chính xác"
            )

        access_token = create_access_token(subject=user["email"])
        logger.info(f"User logged in: {user_in.email}")
        return {"access_token": access_token, "token_type": "bearer"}
