from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database import users_collection
from app.utils.security import hash_password, verify_password, create_jwt_token
from bson import ObjectId

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    password_confirm: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 회원가입 API    
@router.post("/register")
async def register_user(data: RegisterRequest):
    
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    # 이미 존재하는 이메일인지 확인
    existing_user = await users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    # 비밀번호 해싱 후 저장
    hashed_password = hash_password(data.password)
    new_user = {
        "name": data.name,
        "email": data.email,
        "hashed_password": hashed_password,
        "provider": "local",
    }
    await users_collection.insert_one(new_user)
    return {"message": "회원가입이 완료되었습니다."}

# 로그인 API
@router.post("/login")
async def login_user(data: LoginRequest):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="잘못된 이메일 또는 비밀번호입니다.")

    token = create_jwt_token({"sub": str(user["_id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"name": user["name"], "email": user["email"]}
    }
