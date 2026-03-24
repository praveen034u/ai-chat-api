"""
AI Output Parsing and Normalization for Daily Content
"""
import json
from typing import Any, Dict
from app.schemas.daily_content import (
    WordSuggestion, ChallengeSuggestion, AIGenerateDailyContentResponse
)

class DailyContentAIParseError(Exception):
    pass

class DailyContentValidationError(Exception):
    pass

def extract_json_object(text: str) -> Dict:
    """Safely extract JSON object from text, even if surrounded by extra text."""
    try:
        # Try strict parse first
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON substring
        start = text.find('{')
        end = text.rfind('}')
        if start == -1 or end == -1 or end <= start:
            raise DailyContentAIParseError("No valid JSON object found in AI output.")
        try:
            return json.loads(text[start:end+1])
        except Exception as e:
            raise DailyContentAIParseError(f"Malformed JSON: {e}")

def normalize_word_suggestion(data: Dict) -> WordSuggestion:
    try:
        return WordSuggestion(
            word=(data.get("word") or "").strip(),
            meaning=(data.get("meaning") or "").strip(),
            example=(data.get("example") or "").strip(),
            pronunciation=(data.get("pronunciation") or None),
            difficulty=(data.get("difficulty") or None).lower() if data.get("difficulty") else None
        )
    except Exception as e:
        raise DailyContentValidationError(f"Invalid word suggestion: {e}")

def normalize_challenge_suggestion(data: Dict) -> ChallengeSuggestion:
    try:
        return ChallengeSuggestion(
            title=(data.get("title") or "").strip(),
            type=(data.get("type") or "").strip().lower(),
            instructions=(data.get("instructions") or "").strip(),
            estimatedMinutes=int(data.get("estimatedMinutes")),
            difficulty=(data.get("difficulty") or None).lower() if data.get("difficulty") else None
        )
    except Exception as e:
        raise DailyContentValidationError(f"Invalid challenge suggestion: {e}")

def normalize_ai_generation_response(raw_text: str) -> AIGenerateDailyContentResponse:
    try:
        obj = extract_json_object(raw_text)
        if not isinstance(obj, dict):
            raise DailyContentAIParseError("AI output is not a JSON object.")
        word_suggestions = obj.get("wordSuggestions")
        challenge_suggestions = obj.get("challengeSuggestions")
        meta = obj.get("meta", {})
        if not isinstance(word_suggestions, list) or not isinstance(challenge_suggestions, list):
            raise DailyContentAIParseError("Missing or invalid wordSuggestions/challengeSuggestions.")
        words = [normalize_word_suggestion(w) for w in word_suggestions]
        challenges = [normalize_challenge_suggestion(c) for c in challenge_suggestions]
        return AIGenerateDailyContentResponse(
            wordSuggestions=words,
            challengeSuggestions=challenges,
            meta=meta
        )
    except (DailyContentAIParseError, DailyContentValidationError) as e:
        raise
    except Exception as e:
        raise DailyContentAIParseError(f"Failed to normalize AI output: {e}")
