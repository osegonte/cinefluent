from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    native_language: str = "en"
    target_language: str = "de"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProgressBase(BaseModel):
    lesson_id: int
    score: int
    time_spent_seconds: int
    correct_answers: int
    total_questions: int


class UserProgressCreate(UserProgressBase):
    pass


class UserProgress(UserProgressBase):
    id: int
    user_id: int
    completed_at: datetime

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    lessons_completed: int
    total_score: int
    average_score: float
    time_spent_hours: float
    current_streak: int
    words_learned: int
    level: int