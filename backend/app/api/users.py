from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, verify_token
from app.db import crud
from app.db.database import get_db
from app.schemas import users

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user."""
    username = verify_token(credentials.credentials)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = crud.user_crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


@router.post("/register", response_model=users.User)
def register_user(user_data: users.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username exists
    if crud.user_crud.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if crud.user_crud.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = crud.user_crud.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        native_language=user_data.native_language,
        target_language=user_data.target_language
    )
    
    return user


@router.post("/login")
def login_user(login_data: users.UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = crud.user_crud.authenticate_user(db, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=users.User)
def get_current_user_info(current_user: users.User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@router.get("/stats", response_model=users.UserStats)
def get_user_stats(
    current_user: users.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics."""
    stats = crud.progress_crud.get_user_stats(db, current_user.id)
    return stats


@router.post("/progress", response_model=users.UserProgress)
def record_lesson_progress(
    progress_data: users.UserProgressCreate,
    current_user: users.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record completion of a lesson."""
    progress = crud.progress_crud.record_lesson_completion(
        db=db,
        user_id=current_user.id,
        lesson_id=progress_data.lesson_id,
        score=progress_data.score,
        time_spent=progress_data.time_spent_seconds,
        correct=progress_data.correct_answers,
        total=progress_data.total_questions
    )
    
    return progress