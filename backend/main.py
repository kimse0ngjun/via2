from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, career  # interview

app = FastAPI()

# CORS 설정 (라우터 등록 전에 추가)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth")
app.include_router(career.router, prefix="/api/career")
# app.include_router(interview.router, prefix="/api/interview")

# 정적 파일 서빙 (예: favicon.ico 등)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "음 구래구래.."}

# URL: http://127.0.0.1:8000/