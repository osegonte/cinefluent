from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    runtime_min: Optional[int] = None


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
