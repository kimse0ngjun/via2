from fastapi import FastAPI
from app.routes import auth, career # interview

app = FastAPI()

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth")
app.include_router(career.router, prefix="/api/career")
# app.include_router(interview.router, prefix="/api/interview")

@app.get("/")
async def root():
    return {"message": "안녕하세요.."}