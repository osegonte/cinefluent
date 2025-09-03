from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.schemas import lessons

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/")
def get_lessons(
    segment_id: int = Query(..., description="Segment ID to get lessons for"),
    db: Session = Depends(get_db)
):
    """Get all lessons for a segment."""
    lessons_list = crud.lesson_crud.get_lessons_by_segment(db=db, segment_id=segment_id)
    if not lessons_list:
        raise HTTPException(status_code=404, detail="No lessons found for this segment")
    return lessons_list


@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get a specific lesson with its items."""
    lesson = crud.lesson_crud.get_lesson_with_items(db=db, lesson_id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson