from dataclasses import dataclass
from typing import List

from app.services.subtitle_parser import SubtitleLine


@dataclass
class AlignedPair:
    start_ms: int
    end_ms: int
    en_text: str
    de_text: str
    confidence: float


class SubtitleAligner:
    def __init__(self, tolerance_ms: int = 2000):
        """
        tolerance_ms: Maximum time difference to consider subtitles aligned
        """
        self.tolerance_ms = tolerance_ms

    def calculate_overlap(self, line1: SubtitleLine, line2: SubtitleLine) -> float:
        """Calculate time overlap between two subtitle lines (0.0 to 1.0)."""
        start = max(line1.start_ms, line2.start_ms)
        end = min(line1.end_ms, line2.end_ms)
        overlap = max(0, end - start)

        # Calculate as percentage of shorter duration
        duration1 = line1.end_ms - line1.start_ms
        duration2 = line2.end_ms - line2.start_ms
        shorter_duration = min(duration1, duration2)

        if shorter_duration == 0:
            return 0.0

        return overlap / shorter_duration

    def calculate_confidence(
        self, en_line: SubtitleLine, de_line: SubtitleLine
    ) -> float:
        """Calculate confidence score for alignment (0.0 to 1.0)."""
        # Time overlap component
        overlap = self.calculate_overlap(en_line, de_line)

        # Time difference component
        time_diff = abs(en_line.start_ms - de_line.start_ms)
        time_score = max(0, 1.0 - time_diff / self.tolerance_ms)

        # Duration similarity component
        dur1 = en_line.end_ms - en_line.start_ms
        dur2 = de_line.end_ms - de_line.start_ms
        if max(dur1, dur2) == 0:
            duration_score = 1.0
        else:
            duration_score = min(dur1, dur2) / max(dur1, dur2)

        # Weighted average
        confidence = (overlap * 0.5) + (time_score * 0.3) + (duration_score * 0.2)
        return confidence

    def align_subtitles(
        self, en_lines: List[SubtitleLine], de_lines: List[SubtitleLine]
    ) -> List[AlignedPair]:
        """Align English and German subtitle lines."""
        aligned_pairs = []
        used_de_indices = set()

        for en_line in en_lines:
            best_match = None
            best_confidence = 0.0
            best_de_index = -1

            for i, de_line in enumerate(de_lines):
                if i in used_de_indices:
                    continue

                # Check if timing is within tolerance
                time_diff = abs(en_line.start_ms - de_line.start_ms)
                if time_diff > self.tolerance_ms:
                    continue

                confidence = self.calculate_confidence(en_line, de_line)

                if (
                    confidence > best_confidence and confidence > 0.3
                ):  # Minimum confidence threshold
                    best_match = de_line
                    best_confidence = confidence
                    best_de_index = i

            if best_match:
                # Create aligned pair using the overlapping time range
                start_ms = max(en_line.start_ms, best_match.start_ms)
                end_ms = min(en_line.end_ms, best_match.end_ms)

                aligned_pairs.append(
                    AlignedPair(
                        start_ms=start_ms,
                        end_ms=end_ms,
                        en_text=en_line.text,
                        de_text=best_match.text,
                        confidence=best_confidence,
                    )
                )
                used_de_indices.add(best_de_index)

        return aligned_pairs


# Global instance
aligner = SubtitleAligner()
