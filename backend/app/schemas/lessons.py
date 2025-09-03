from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LessonItemBase(BaseModel):
    payload_json: str  # JSON string containing question, options, answers


class LessonItemCreate(LessonItemBase):
    lesson_id: int


class LessonItem(LessonItemBase):
    id: int
    lesson_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    segment_id: int
    kind: str  # vocab_mcq, cloze, match_lines, drag_drop


class LessonCreate(LessonBase):
    pass


class Lesson(LessonBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LessonWithItems(Lesson):
    lesson_items: List[LessonItem] = []