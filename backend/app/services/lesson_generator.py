import json
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.services.segmentation import Segment, AlignedPair

@dataclass
class LessonItem:
    question: str
    options: List[str] = None  # For MCQ
    correct_answer: str = ""
    explanation: str = ""
    difficulty: str = "medium"  # easy, medium, hard

@dataclass
class Lesson:
    segment_id: int
    lesson_type: str  # vocab_mcq, cloze, match_lines, drag_drop
    items: List[LessonItem]
    total_points: int

class LessonGenerator:
    def __init__(self):
        # Basic word frequency lists for vocabulary selection
        self.common_words = {
            'en': ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'have', 'has', 'do', 'does', 'will', 'would'],
            'de': ['der', 'die', 'das', 'ein', 'eine', 'ist', 'sind', 'war', 'waren', 'haben', 'hat']
        }
        
        self.target_words = {
            'en': ['become', 'friend', 'believe', 'protect', 'strong', 'training', 'dreams', 'mission'],
            'de': ['werden', 'freund', 'glauben', 'beschützen', 'stark', 'training', 'träume', 'mission']
        }
    
    def generate_all_lessons_for_segment(self, segment: Segment) -> List[Lesson]:
        """Generate all lesson types for a segment."""
        lessons = []
        
        # Generate different lesson types
        lessons.append(self.generate_vocab_mcq(segment))
        lessons.append(self.generate_cloze_lesson(segment))
        lessons.append(self.generate_matching_lesson(segment))
        lessons.append(self.generate_drag_drop_lesson(segment))
        
        return lessons
    
    def generate_vocab_mcq(self, segment: Segment) -> Lesson:
        """Generate vocabulary multiple choice questions."""
        items = []
        pairs = segment.pairs
        
        # Find interesting words for vocabulary questions
        for i, pair in enumerate(pairs[:5]):  # Limit to 5 questions
            en_words = pair.en_text.lower().replace(',', '').replace('.', '').replace('!', '').split()
            de_words = pair.de_text.lower().replace(',', '').replace('.', '').replace('!', '').split()
            
            # Find a good target word (not too common, not too rare)
            target_word = None
            target_translation = None
            
            for j, en_word in enumerate(en_words):
                if (en_word not in self.common_words['en'] and 
                    len(en_word) > 3 and 
                    j < len(de_words)):
                    target_word = en_word
                    target_translation = de_words[j] if j < len(de_words) else de_words[0]
                    break
            
            if target_word and target_translation:
                # Generate distractors
                other_de_words = []
                for other_pair in pairs:
                    words = other_pair.de_text.lower().replace(',', '').replace('.', '').replace('!', '').split()
                    other_de_words.extend([w for w in words if w != target_translation and len(w) > 2])
                
                # Create MCQ options
                options = [target_translation]
                random.shuffle(other_de_words)
                for word in other_de_words[:3]:  # Add 3 distractors
                    if word not in options:
                        options.append(word)
                
                if len(options) == 4:  # Ensure we have exactly 4 options
                    random.shuffle(options)
                    
                    items.append(LessonItem(
                        question=f'What does "{target_word}" mean in German?',
                        options=options,
                        correct_answer=target_translation,
                        explanation=f'In the context: "{pair.en_text}" → "{pair.de_text}"'
                    ))
        
        return Lesson(
            segment_id=segment.index,
            lesson_type="vocab_mcq",
            items=items,
            total_points=len(items) * 10
        )
    
    def generate_cloze_lesson(self, segment: Segment) -> Lesson:
        """Generate fill-in-the-blank (cloze) exercises."""
        items = []
        
        for i, pair in enumerate(segment.pairs[:4]):  # Limit to 4 questions
            de_words = pair.de_text.split()
            
            # Find a good word to blank out (not too common, not first/last word)
            target_idx = None
            target_word = None
            
            for j, word in enumerate(de_words):
                clean_word = word.lower().replace(',', '').replace('.', '').replace('!', '')
                if (j > 0 and j < len(de_words) - 1 and 
                    clean_word not in self.common_words.get('de', []) and 
                    len(clean_word) > 3):
                    target_idx = j
                    target_word = word
                    break
            
            if target_idx is not None and target_word:
                # Create the cloze sentence
                cloze_words = de_words.copy()
                cloze_words[target_idx] = "______"
                cloze_sentence = " ".join(cloze_words)
                
                items.append(LessonItem(
                    question=f'Fill in the blank: {cloze_sentence}',
                    correct_answer=target_word.replace(',', '').replace('.', '').replace('!', ''),
                    explanation=f'English context: "{pair.en_text}"'
                ))
        
        return Lesson(
            segment_id=segment.index,
            lesson_type="cloze",
            items=items,
            total_points=len(items) * 15
        )
    
    def generate_matching_lesson(self, segment: Segment) -> Lesson:
        """Generate line matching exercises."""
        items = []
        pairs = segment.pairs[:5]  # Use first 5 pairs
        
        if len(pairs) >= 3:
            # Create matching exercise
            en_lines = [pair.en_text for pair in pairs]
            de_lines = [pair.de_text for pair in pairs]
            
            # Shuffle the German lines
            shuffled_de = de_lines.copy()
            random.shuffle(shuffled_de)
            
            # Create the matching question
            question_parts = []
            question_parts.append("Match the English lines with their German translations:")
            question_parts.append("\nEnglish:")
            for i, en_line in enumerate(en_lines, 1):
                question_parts.append(f"{i}. {en_line}")
            
            question_parts.append("\nGerman:")
            for i, de_line in enumerate(shuffled_de, 1):
                question_parts.append(f"{chr(65+i-1)}. {de_line}")  # A, B, C, etc.
            
            # Create answer key
            answer_key = {}
            for i, en_line in enumerate(en_lines, 1):
                corresponding_de = de_lines[i-1]
                de_letter = chr(65 + shuffled_de.index(corresponding_de))
                answer_key[str(i)] = de_letter
            
            items.append(LessonItem(
                question="\n".join(question_parts),
                correct_answer=json.dumps(answer_key),
                explanation="Match each English line with its German translation based on meaning."
            ))
        
        return Lesson(
            segment_id=segment.index,
            lesson_type="match_lines",
            items=items,
            total_points=len(pairs) * 5
        )
    
    def generate_drag_drop_lesson(self, segment: Segment) -> Lesson:
        """Generate drag-and-drop word order exercises."""
        items = []
        
        for i, pair in enumerate(segment.pairs[:3]):  # Limit to 3 questions
            de_sentence = pair.de_text
            words = de_sentence.split()
            
            if len(words) >= 4:  # Only for sentences with 4+ words
                # Shuffle the words
                shuffled_words = words.copy()
                random.shuffle(shuffled_words)
                
                items.append(LessonItem(
                    question=f'Arrange these German words in the correct order:\n{" | ".join(shuffled_words)}',
                    correct_answer=" ".join(words),
                    explanation=f'English: "{pair.en_text}"'
                ))
        
        return Lesson(
            segment_id=segment.index,
            lesson_type="drag_drop",
            items=items,
            total_points=len(items) * 20
        )

# Global instance
lesson_generator = LessonGenerator()