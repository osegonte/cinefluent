from sqlalchemy.orm import Session
from app.db import models
from app.core.auth import get_password_hash, verify_password
from datetime import datetime, timedelta


class MovieCRUD:
    def create_movie(
        self, db: Session, title: str, year: int = None, runtime_min: int = None
    ):
        db_movie = models.Movie(title=title, year=year, runtime_min=runtime_min)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    def get_movie(self, db: Session, movie_id: int):
        return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    def get_movies(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Movie).offset(skip).limit(limit).all()

    def delete_movie(self, db: Session, movie_id: int):
        movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
        if movie:
            db.delete(movie)
            db.commit()
        return movie


class SegmentCRUD:
    def create_segment(
        self, db: Session, movie_id: int, index: int, start_ms: int, end_ms: int, type: str = "minute"
    ):
        db_segment = models.Segment(
            movie_id=movie_id, index=index, start_ms=start_ms, end_ms=end_ms, type=type
        )
        db.add(db_segment)
        db.commit()
        db.refresh(db_segment)
        return db_segment

    def get_segment(self, db: Session, segment_id: int):
        return db.query(models.Segment).filter(models.Segment.id == segment_id).first()

    def get_segments_by_movie(self, db: Session, movie_id: int):
        return db.query(models.Segment).filter(models.Segment.movie_id == movie_id).order_by(models.Segment.index).all()


class LessonCRUD:
    def create_lesson(self, db: Session, segment_id: int, kind: str):
        db_lesson = models.Lesson(segment_id=segment_id, kind=kind)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson

    def create_lesson_item(self, db: Session, lesson_id: int, payload_json: str):
        db_item = models.LessonItem(lesson_id=lesson_id, payload_json=payload_json)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def get_lesson(self, db: Session, lesson_id: int):
        return db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()

    def get_lessons_by_segment(self, db: Session, segment_id: int):
        return db.query(models.Lesson).filter(models.Lesson.segment_id == segment_id).all()

    def get_lesson_with_items(self, db: Session, lesson_id: int):
        lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
        if lesson:
            # Load the lesson_items relationship
            lesson.lesson_items  # This triggers the lazy loading
        return lesson


class UserCRUD:
    def create_user(self, db: Session, username: str, email: str, password: str, 
                   native_language: str = "en", target_language: str = "de"):
        hashed_password = get_password_hash(password)
        db_user = models.User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            native_language=native_language,
            target_language=target_language
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create initial streak records
        self._create_initial_streaks(db, db_user.id)
        
        return db_user

    def get_user_by_username(self, db: Session, username: str):
        return db.query(models.User).filter(models.User.username == username).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def authenticate_user(self, db: Session, username: str, password: str):
        user = self.get_user_by_username(db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user

    def _create_initial_streaks(self, db: Session, user_id: int):
        """Create initial streak records for a new user."""
        streak_types = ["daily_lesson", "weekly_goal"]
        for streak_type in streak_types:
            streak = models.UserStreak(
                user_id=user_id,
                streak_type=streak_type,
                current_count=0,
                best_count=0
            )
            db.add(streak)
        db.commit()


class UserProgressCRUD:
    def record_lesson_completion(self, db: Session, user_id: int, lesson_id: int,
                                score: int, time_spent: int, correct: int, total: int):
        progress = models.UserProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            score=score,
            time_spent_seconds=time_spent,
            correct_answers=correct,
            total_questions=total
        )
        db.add(progress)
        db.commit()
        
        # Update streaks
        self._update_streaks(db, user_id)
        
        return progress

    def get_user_stats(self, db: Session, user_id: int):
        """Get comprehensive user statistics."""
        progress_records = db.query(models.UserProgress).filter(
            models.UserProgress.user_id == user_id
        ).all()
        
        if not progress_records:
            return {
                "lessons_completed": 0,
                "total_score": 0,
                "average_score": 0.0,
                "time_spent_hours": 0.0,
                "current_streak": 0,
                "words_learned": 0,
                "level": 1
            }
        
        lessons_completed = len(progress_records)
        total_score = sum(p.score for p in progress_records)
        total_time = sum(p.time_spent_seconds for p in progress_records)
        average_score = total_score / lessons_completed if lessons_completed > 0 else 0
        
        # Get current daily streak
        daily_streak = db.query(models.UserStreak).filter(
            models.UserStreak.user_id == user_id,
            models.UserStreak.streak_type == "daily_lesson"
        ).first()
        
        current_streak = daily_streak.current_count if daily_streak else 0
        
        # Count learned words (strength >= 2)
        words_learned = db.query(models.UserWord).filter(
            models.UserWord.user_id == user_id,
            models.UserWord.strength >= 2
        ).count()
        
        # Calculate level (simple: every 1000 points = 1 level)
        level = max(1, total_score // 1000 + 1)
        
        return {
            "lessons_completed": lessons_completed,
            "total_score": total_score,
            "average_score": round(average_score, 1),
            "time_spent_hours": round(total_time / 3600, 1),
            "current_streak": current_streak,
            "words_learned": words_learned,
            "level": level
        }

    def _update_streaks(self, db: Session, user_id: int):
        """Update user streak counters."""
        today = datetime.utcnow().date()
        
        # Update daily lesson streak
        daily_streak = db.query(models.UserStreak).filter(
            models.UserStreak.user_id == user_id,
            models.UserStreak.streak_type == "daily_lesson"
        ).first()
        
        if daily_streak:
            last_activity_date = daily_streak.last_activity.date() if daily_streak.last_activity else None
            
            if last_activity_date == today:
                # Already completed today, don't increment
                pass
            elif last_activity_date == today - timedelta(days=1):
                # Completed yesterday, increment streak
                daily_streak.current_count += 1
                daily_streak.best_count = max(daily_streak.best_count, daily_streak.current_count)
            else:
                # Streak broken, reset to 1
                daily_streak.current_count = 1
            
            daily_streak.last_activity = datetime.utcnow()
            db.commit()



# Global instances
movie_crud = MovieCRUD()
segment_crud = SegmentCRUD()
lesson_crud = LessonCRUD()
user_crud = UserCRUD()
progress_crud = UserProgressCRUD()