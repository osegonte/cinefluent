from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for segment_pairs (many-to-many)
segment_pairs_table = Table(
    "segment_pairs",
    Base.metadata,
    Column("segment_id", Integer, ForeignKey("segments.id")),
    Column("pair_id", Integer, ForeignKey("aligned_pairs.id")),
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    runtime_min = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    subtitles = relationship("Subtitle", back_populates="movie")
    aligned_pairs = relationship("AlignedPair", back_populates="movie")
    segments = relationship("Segment", back_populates="movie")


class Subtitle(Base):
    __tablename__ = "subtitles"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    lang = Column(String(5), nullable=False)  # en, de, etc.
    source = Column(String)  # file source info
    raw_text = Column(Text)
    format = Column(String)  # srt, vtt, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    movie = relationship("Movie", back_populates="subtitles")
    subtitle_lines = relationship("SubtitleLine", back_populates="subtitle")


class SubtitleLine(Base):
    __tablename__ = "subtitle_lines"

    id = Column(Integer, primary_key=True, index=True)
    subtitle_id = Column(Integer, ForeignKey("subtitles.id"))
    movie_id = Column(
        Integer, ForeignKey("movies.id")
    )  # denormalized for easier queries
    lang = Column(String(5), nullable=False)
    start_ms = Column(Integer, nullable=False)
    end_ms = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    # Relationships
    subtitle = relationship("Subtitle", back_populates="subtitle_lines")


class AlignedPair(Base):
    __tablename__ = "aligned_pairs"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    start_ms = Column(Integer, nullable=False)
    end_ms = Column(Integer, nullable=False)
    en_text = Column(Text, nullable=False)
    de_text = Column(Text, nullable=False)
    align_conf = Column(Float)  # confidence score
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    movie = relationship("Movie", back_populates="aligned_pairs")
    segments = relationship(
        "Segment", secondary=segment_pairs_table, back_populates="pairs"
    )


class Segment(Base):
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    index = Column(Integer, nullable=False)  # segment number
    start_ms = Column(Integer, nullable=False)
    end_ms = Column(Integer, nullable=False)
    type = Column(String, default="minute")  # minute, scene, custom
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    movie = relationship("Movie", back_populates="segments")
    pairs = relationship(
        "AlignedPair", secondary=segment_pairs_table, back_populates="segments"
    )
    lessons = relationship("Lesson", back_populates="segment")


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    lang = Column(String(5), nullable=False)
    lemma = Column(String, nullable=False)
    display = Column(String, nullable=False)
    freq_band = Column(Integer)  # 1=most common, higher=less common
    cefr = Column(String(2))  # A1, A2, B1, B2, C1, C2
    created_at = Column(DateTime, default=datetime.utcnow)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("segments.id"))
    kind = Column(String, nullable=False)  # vocab_mcq, cloze, match_lines, drag_drop
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    segment = relationship("Segment", back_populates="lessons")
    lesson_items = relationship("LessonItem", back_populates="lesson")


class LessonItem(Base):
    __tablename__ = "lesson_items"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    payload_json = Column(Text)  # JSON string with prompts/options/answers
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    lesson = relationship("Lesson", back_populates="lesson_items")


# NEW USER SYSTEM MODELS

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(100), nullable=False)
    native_language = Column(String(5), default="en")  # User's native language
    target_language = Column(String(5), default="de")  # Language they're learning
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    progress = relationship("UserProgress", back_populates="user")
    words = relationship("UserWord", back_populates="user")
    streaks = relationship("UserStreak", back_populates="user")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer)  # Points earned
    time_spent_seconds = Column(Integer)  # Time spent on lesson
    correct_answers = Column(Integer)
    total_questions = Column(Integer)

    # Relationships
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson")


class UserWord(Base):
    __tablename__ = "user_words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    
    # Spaced repetition system (SRS) data
    strength = Column(Integer, default=0)  # 0=new, 1=learning, 2=known, 3=mastered
    interval_days = Column(Integer, default=1)  # Days until next review
    ease_factor = Column(Float, default=2.5)  # SuperMemo ease factor
    repetitions = Column(Integer, default=0)  # Number of successful reviews
    
    next_review = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="words")
    word = relationship("Word")


class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    streak_type = Column(String(20))  # daily_lesson, weekly_goal, etc.
    current_count = Column(Integer, default=0)
    best_count = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="streaks")