from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, career # interview

app = FastAPI()

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth")
app.include_router(career.router, prefix="/api/career")
# app.include_router(interview.router, prefix="/api/interview")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

@app.post("/register")
async def register(data: dict):
    # 회원가입 처리 로직
    return {"message": "회원가입 성공!"}
# 정적 파일 (favicon.ico) 서빙 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "안녕하세요.."}

# URL: http://127.0.0.1:8000/