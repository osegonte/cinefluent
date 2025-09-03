import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import requests

@dataclass
class LanguageAnalysis:
    language_code: str
    language_name: str
    difficulty_level: str  # beginner, intermediate, advanced
    learning_notes: str
    recommended_as_source: bool
    recommended_as_target: bool

class DeepSeekClient:
    BASE_URL = "https://api.deepseek.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def analyze_language_options(
        self, 
        available_languages: List[str], 
        user_native_language: str = "en"
    ) -> List[LanguageAnalysis]:
        """Analyze available subtitle languages and provide learning recommendations."""
        
        prompt = f"""
        Analyze these available subtitle languages for a language learning app:
        Available languages: {', '.join(available_languages)}
        User's native language: {user_native_language}
        
        For each language, provide analysis in this exact JSON format:
        [
          {{
            "language_code": "de",
            "language_name": "German",
            "difficulty_level": "intermediate",
            "learning_notes": "Good for English speakers due to shared Germanic roots",
            "recommended_as_source": false,
            "recommended_as_target": true
          }}
        ]
        
        Return only the JSON array, no other text.
        """
        
        try:
            response = self.session.post(
                f"{self.BASE_URL}/chat/completions",
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000
                },
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            
            # Clean up the response to extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse JSON response
            analyses_data = json.loads(content)
            
            analyses = []
            for data in analyses_data:
                analyses.append(LanguageAnalysis(
                    language_code=data["language_code"],
                    language_name=data["language_name"],
                    difficulty_level=data["difficulty_level"],
                    learning_notes=data["learning_notes"],
                    recommended_as_source=data["recommended_as_source"],
                    recommended_as_target=data["recommended_as_target"]
                ))
            
            return analyses
            
        except Exception as e:
            print(f"DeepSeek API error: {e}")
            # Fallback to basic analysis if API fails
            return self._fallback_analysis(available_languages, user_native_language)
    
    def suggest_language_pairs(
        self, 
        analyses: List[LanguageAnalysis],
        user_level: str = "beginner"
    ) -> List[Dict[str, str]]:
        """Suggest optimal source->target language pairs for learning."""
        
        pairs = []
        
        # Find good source languages (usually native or well-known)
        source_candidates = [a for a in analyses if a.recommended_as_source or a.language_code == "en"]
        target_candidates = [a for a in analyses if a.recommended_as_target]
        
        for source in source_candidates:
            for target in target_candidates:
                if source.language_code != target.language_code:
                    # Skip if difficulty doesn't match user level
                    if user_level == "beginner" and target.difficulty_level == "advanced":
                        continue
                    
                    pairs.append({
                        "source_code": source.language_code,
                        "source_name": source.language_name,
                        "target_code": target.language_code,
                        "target_name": target.language_name,
                        "difficulty": target.difficulty_level,
                        "notes": target.learning_notes
                    })
        
        return pairs
    
    def _fallback_analysis(
        self, 
        languages: List[str], 
        native_lang: str
    ) -> List[LanguageAnalysis]:
        """Provide basic analysis when API is unavailable."""
        
        basic_info = {
            "en": ("English", "beginner", "Universal language", True, False),
            "de": ("German", "intermediate", "Good for English speakers", False, True),
            "fr": ("French", "intermediate", "Romance language with English influence", False, True),
            "es": ("Spanish", "beginner", "Phonetic and regular grammar", False, True),
            "it": ("Italian", "beginner", "Melodic Romance language", False, True),
            "pt": ("Portuguese", "intermediate", "Similar to Spanish", False, True),
            "ru": ("Russian", "advanced", "Cyrillic script, complex grammar", False, True),
            "ja": ("Japanese", "advanced", "Multiple writing systems", False, True),
            "ko": ("Korean", "advanced", "Unique grammar structure", False, True),
            "zh": ("Chinese", "advanced", "Tonal language", False, True),
            "ar": ("Arabic", "advanced", "Right-to-left script", False, True),
            "hi": ("Hindi", "intermediate", "Devanagari script", False, True),
            "nl": ("Dutch", "intermediate", "Similar to German and English", False, True),
            "sv": ("Swedish", "intermediate", "Germanic language", False, True),
            "no": ("Norwegian", "intermediate", "Germanic language", False, True),
            "da": ("Danish", "intermediate", "Germanic language", False, True),
            "fi": ("Finnish", "advanced", "Unique grammar structure", False, True),
            "pl": ("Polish", "advanced", "Complex grammar", False, True),
            "tr": ("Turkish", "advanced", "Agglutinative language", False, True)
        }
        
        analyses = []
        for lang in languages:
            if lang in basic_info:
                name, difficulty, notes, rec_source, rec_target = basic_info[lang]
                analyses.append(LanguageAnalysis(
                    language_code=lang,
                    language_name=name,
                    difficulty_level=difficulty,
                    learning_notes=notes,
                    recommended_as_source=rec_source or lang == native_lang,
                    recommended_as_target=rec_target and lang != native_lang
                ))
            else:
                # Unknown language fallback
                analyses.append(LanguageAnalysis(
                    language_code=lang,
                    language_name=lang.upper(),
                    difficulty_level="intermediate",
                    learning_notes="Language analysis not available",
                    recommended_as_source=lang == native_lang,
                    recommended_as_target=lang != native_lang
                ))
        
        return analyses

# Global instance
deepseek_client: Optional[DeepSeekClient] = None

def get_deepseek_client() -> DeepSeekClient:
    global deepseek_client
    if not deepseek_client:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        deepseek_client = DeepSeekClient(api_key)
    return deepseek_client