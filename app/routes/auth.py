from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database import users_collection
from app.utils.security import hash_password, verify_password, create_jwt_token, verify_jwt_token
from bson import ObjectId

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

    token = create_jwt_token({"sub": str(user["_id"]), "user_id": str(user["_id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"name": user["name"], "email": user["email"]}
    }

# 로그인 상태 확인
@router.get("/status")
async def get_login_status(token: str = Depends(oauth2_scheme)):
    payload = verify_jwt_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="토근이 만료되었습니다."
        )
    
    return {"status": "success", "user_id": payload["user_id"], "message": "성공적으로 로그인 되었습니다."}
