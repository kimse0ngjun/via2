from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

# 학생 모델
class StudentCreate(BaseModel):
    user_id: str
    age: int
    gender: str
    grade: int
    interest_IT: str
    job: str
    qualifications: List[str]
    interest: str
    target_company: str
    save_history: bool = True

# 대화 모델
class ConversationCreate(BaseModel):
    user_id: str
    topic: str
    created_at: datetime = datetime.now(timezone.utc)
    is_deleted: bool = False

# 채팅 모델
class ChatCreate(BaseModel):
    con_id: str
    user_message: str
    gpt_reply: str
    created_at: datetime = datetime.now(timezone.utc)
