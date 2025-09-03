from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SegmentBase(BaseModel):
    movie_id: int
    index: int
    start_ms: int
    end_ms: int
    type: str = "minute"


class SegmentCreate(SegmentBase):
    pass


class Segment(SegmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True