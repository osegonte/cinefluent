import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SubtitleLine:
    start_ms: int
    end_ms: int
    text: str


class SubtitleParser:
    def __init__(self):
        self.srt_pattern = re.compile(
            r"(\d+)\n(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})\n(.*?)(?=\n\n|\n\d|\Z)",
            re.DOTALL,
        )

    def time_to_ms(
        self, hours: int, minutes: int, seconds: int, milliseconds: int
    ) -> int:
        """Convert time components to milliseconds."""
        return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

    def parse_srt(self, content: str) -> List[SubtitleLine]:
        """Parse SRT subtitle format."""
        lines = []
        matches = self.srt_pattern.findall(content)

        for match in matches:
            _, h1, m1, s1, ms1, h2, m2, s2, ms2, text = match

            start_ms = self.time_to_ms(int(h1), int(m1), int(s1), int(ms1))
            end_ms = self.time_to_ms(int(h2), int(m2), int(s2), int(ms2))

            # Clean text (remove HTML tags, extra whitespace)
            clean_text = re.sub(r"<[^>]+>", "", text).strip()
            clean_text = re.sub(r"\n+", " ", clean_text)

            if clean_text:  # Only add non-empty lines
                lines.append(SubtitleLine(start_ms, end_ms, clean_text))

        return lines

    def parse_file(self, file_path: str) -> List[SubtitleLine]:
        """Parse subtitle file based on extension."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Subtitle file not found: {file_path}")

        content = path.read_text(encoding="utf-8")

        if path.suffix.lower() == ".srt":
            return self.parse_srt(content)
        else:
            raise ValueError(f"Unsupported subtitle format: {path.suffix}")


# Global instance
subtitle_parser = SubtitleParser()
