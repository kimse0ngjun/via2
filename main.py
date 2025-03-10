from fastapi import FastAPI
from app.routes import auth, career, interview

app = FastAPI()

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth")
app.include_router(career.router, prefix="/api")
# app.include_router(interview.router, prefix="/api")

@app.get("/")
async def root():
    return {"진로 상담 API가 실행 중입니다."}

