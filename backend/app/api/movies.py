from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.schemas import movies

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/", response_model=movies.Movie)
def create_movie(movie: movies.MovieCreate, db: Session = Depends(get_db)):
    return crud.movie_crud.create_movie(
        db=db, title=movie.title, year=movie.year, runtime_min=movie.runtime_min
    )


@router.get("/", response_model=List[movies.Movie])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.movie_crud.get_movies(db=db, skip=skip, limit=limit)


@router.get("/{movie_id}", response_model=movies.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.movie_crud.get_movie(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.movie_crud.delete_movie(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted"}
