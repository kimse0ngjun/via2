from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.security import hash_password, verify_password, create_jwt_token
from app.database import users_collection
from app.models.user import UserCreate, UserLogin, UserResponse

router = APIRouter()

# 회원가입 API
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await users_collection.find_one({"userid": user.userid})
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    
    hashed_password = hash_password(user.password)
    user_data = {"userid": user.userid, "password": hashed_password}
    await users_collection.insert_one(user_data)

    return UserResponse(userid=user.userid)

# 로그인 API
@router.post("/login")
async def login(user: UserLogin):
    existing_user = await users_collection.find_one({"userid": user.userid})
    if not existing_user:
        raise HTTPException(status_code=400, detail="존재하지 않는 사용자입니다.")
    
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    
    token = create_jwt_token({"userid": user.userid})
    return {"access_token": token, "token_type": "bearer"}