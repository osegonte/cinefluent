#!/usr/bin/env python3

import sys
import json
import argparse
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.services.subtitle_parser import subtitle_parser
from app.services.alignment import aligner
from app.services.segmentation import segmenter
from app.services.lesson_generator import lesson_generator
from app.db.database import SessionLocal
from app.db import crud

def process_and_store_complete_movie(
    en_file: str, 
    de_file: str, 
    movie_title: str, 
    year: int = None
):
    """Process subtitle files and store everything in database."""
    
    print(f"🎬 Processing '{movie_title}' for database storage...")
    
    db = SessionLocal()
    try:
        # Step 1: Create movie entry
        print("📚 Creating movie entry...")
        movie = crud.movie_crud.create_movie(
            db=db, title=movie_title, year=year
        )
        print(f"  Created movie: {movie.title} (ID: {movie.id})")
        
        # Step 2: Process subtitles through pipeline
        print("⚙️  Processing subtitles...")
        en_lines = subtitle_parser.parse_file(en_file)
        de_lines = subtitle_parser.parse_file(de_file)
        
        print(f"  Parsed {len(en_lines)} EN lines, {len(de_lines)} DE lines")
        
        aligned_pairs = aligner.align_subtitles(en_lines, de_lines)
        print(f"  Aligned {len(aligned_pairs)} pairs")
        
        segments = segmenter.create_minute_segments(aligned_pairs)
        print(f"  Created {len(segments)} segments")
        
        # Step 3: Store segments
        print("💾 Storing segments...")
        db_segments = []
        for segment in segments:
            db_segment = crud.segment_crud.create_segment(
                db=db,
                movie_id=movie.id,
                index=segment.index,
                start_ms=segment.start_ms,
                end_ms=segment.end_ms,
                type=segment.type
            )
            db_segments.append(db_segment)
            print(f"  Segment {segment.index}: {len(segment.pairs)} pairs")
        
        # Step 4: Generate and store lessons
        print("🎯 Generating and storing lessons...")
        total_lessons = 0
        total_items = 0
        
        for i, segment in enumerate(segments):
            print(f"  Processing segment {segment.index}...")
            lessons = lesson_generator.generate_all_lessons_for_segment(segment)
            
            for lesson in lessons:
                # Create lesson in DB
                db_lesson = crud.lesson_crud.create_lesson(
                    db=db,
                    segment_id=db_segments[i].id,
                    kind=lesson.lesson_type
                )
                
                # Store lesson items
                for item in lesson.items:
                    # Convert lesson item to JSON
                    item_data = {
                        "question": item.question,
                        "options": item.options,
                        "correct_answer": item.correct_answer,
                        "explanation": item.explanation,
                        "difficulty": item.difficulty
                    }
                    
                    crud.lesson_crud.create_lesson_item(
                        db=db,
                        lesson_id=db_lesson.id,
                        payload_json=json.dumps(item_data)
                    )
                    total_items += 1
                
                total_lessons += 1
                print(f"    {lesson.lesson_type}: {len(lesson.items)} items")
        
        print(f"\n✅ Complete! Stored:")
        print(f"  🎬 Movie: {movie.title}")
        print(f"  📊 Segments: {len(segments)}")
        print(f"  📚 Lessons: {total_lessons}")
        print(f"  🎯 Lesson Items: {total_items}")
        
        return {
            "movie_id": movie.id,
            "segments": len(segments),
            "lessons": total_lessons,
            "items": total_items
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Process subtitles and store complete movie data")
    parser.add_argument("en_file", help="English subtitle file path")
    parser.add_argument("de_file", help="German subtitle file path")
    parser.add_argument("--title", required=True, help="Movie title")
    parser.add_argument("--year", type=int, help="Release year")
    
    args = parser.parse_args()
    
    result = process_and_store_complete_movie(
        args.en_file, 
        args.de_file, 
        args.title, 
        args.year
    )
    
    print(f"\n🚀 Ready for API testing!")
    print(f"  GET /api/v1/movies -> Should show '{args.title}'")
    print(f"  GET /api/v1/segments?movie_id={result['movie_id']} -> Should show segments")
    print(f"  GET /api/v1/lessons?segment_id=<id> -> Should show lessons")

if __name__ == "__main__":
    main()