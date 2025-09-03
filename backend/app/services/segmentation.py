from dataclasses import dataclass
from typing import List

from app.services.alignment import AlignedPair


@dataclass
class Segment:
    index: int
    start_ms: int
    end_ms: int
    pairs: List[AlignedPair]
    type: str = "minute"


class Segmenter:
    def __init__(self, segment_duration_ms: int = 60000):  # 1 minute default
        self.segment_duration_ms = segment_duration_ms

    def create_minute_segments(self, aligned_pairs: List[AlignedPair]) -> List[Segment]:
        """Create segments based on time intervals (minute buckets)."""
        if not aligned_pairs:
            return []

        # Find the total time range
        start_time = min(pair.start_ms for pair in aligned_pairs)
        end_time = max(pair.end_ms for pair in aligned_pairs)

        segments = []
        current_time = start_time
        segment_index = 0

        while current_time < end_time:
            segment_end = current_time + self.segment_duration_ms

            # Find pairs that fall within this segment
            segment_pairs = []
            for pair in aligned_pairs:
                # Include if there's any overlap with the segment
                if pair.start_ms < segment_end and pair.end_ms > current_time:
                    segment_pairs.append(pair)

            if segment_pairs:  # Only create segment if it has content
                actual_start = min(pair.start_ms for pair in segment_pairs)
                actual_end = max(pair.end_ms for pair in segment_pairs)

                segments.append(
                    Segment(
                        index=segment_index,
                        start_ms=actual_start,
                        end_ms=actual_end,
                        pairs=segment_pairs,
                        type="minute",
                    )
                )
                segment_index += 1

            current_time = segment_end

        return segments

    def create_custom_segments(
        self, aligned_pairs: List[AlignedPair], break_points_ms: List[int]
    ) -> List[Segment]:
        """Create segments based on custom break points."""
        if not aligned_pairs or not break_points_ms:
            return self.create_minute_segments(aligned_pairs)

        segments = []
        break_points = sorted(break_points_ms)

        for i, break_point in enumerate(break_points[:-1]):
            start_time = break_point
            end_time = break_points[i + 1]

            # Find pairs within this range
            segment_pairs = []
            for pair in aligned_pairs:
                if pair.start_ms >= start_time and pair.end_ms <= end_time:
                    segment_pairs.append(pair)

            if segment_pairs:
                segments.append(
                    Segment(
                        index=i,
                        start_ms=start_time,
                        end_ms=end_time,
                        pairs=segment_pairs,
                        type="custom",
                    )
                )

        return segments


# Global instance
segmenter = Segmenter()
