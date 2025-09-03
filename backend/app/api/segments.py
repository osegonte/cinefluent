from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.schemas import segments

router = APIRouter(prefix="/segments", tags=["segments"])


@router.get("/")
def get_segments(
    movie_id: int = Query(..., description="Movie ID to get segments for"),
    db: Session = Depends(get_db)
):
    """Get all segments for a movie."""
    segments_list = crud.segment_crud.get_segments_by_movie(db=db, movie_id=movie_id)
    if not segments_list:
        raise HTTPException(status_code=404, detail="No segments found for this movie")
    return segments_list


@router.get("/{segment_id}")
def get_segment(segment_id: int, db: Session = Depends(get_db)):
    """Get a specific segment."""
    segment = crud.segment_crud.get_segment(db=db, segment_id=segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment