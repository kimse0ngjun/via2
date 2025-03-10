# user.py
from pydantic import BaseModel

# 회원가입 요청 모델
class UserCreate(BaseModel):
    username: str
    userid: str
    password: str
    repassword: str

class UserLogin(BaseModel):
    userid: str
    password: str

class UserResponse(BaseModel):
    username: str