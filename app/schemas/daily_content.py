"""
Strict Pydantic Schemas for Teacher Daily Content
"""
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict
from datetime import date, datetime

CHALLENGE_TYPES = {"writing", "speaking", "vocabulary", "mixed"}

def not_blank(v: str) -> str:
    if not v or not v.strip():
        raise ValueError("Field cannot be blank.")
    return v.strip()

class AIGenerateDailyContentRequest(BaseModel):
    classId: str = Field(..., min_length=1)
    gradeLevel: str = Field(..., min_length=1)
    contentDate: date
    studentAgeGroup: Optional[str] = None
    subject: Optional[str] = None
    theme: Optional[str] = None
    teacherInstructions: Optional[str] = None
    challengeTypes: List[str] = Field(default_factory=lambda: ["writing", "speaking", "vocabulary"])
    countPerType: int = 3

    @validator("classId", "gradeLevel", pre=True)
    def validate_not_blank(cls, v):
        return not_blank(v)

    @validator("challengeTypes", each_item=True)
    def validate_challenge_type(cls, v):
        v = v.strip().lower()
        if v not in CHALLENGE_TYPES:
            raise ValueError(f"Invalid challenge type: {v}")
        return v

class WordSuggestion(BaseModel):
    word: str = Field(..., max_length=50)
    meaning: str = Field(..., max_length=300)
    example: str = Field(..., max_length=300)
    pronunciation: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, max_length=20)

    _not_blank_word = validator("word", allow_reuse=True)(not_blank)
    _not_blank_meaning = validator("meaning", allow_reuse=True)(not_blank)
    _not_blank_example = validator("example", allow_reuse=True)(not_blank)

class ChallengeSuggestion(BaseModel):
    title: str = Field(..., max_length=120)
    type: str = Field(...)
    instructions: str = Field(..., max_length=1000)
    estimatedMinutes: int = Field(..., ge=1, le=15)
    difficulty: Optional[str] = Field(None, max_length=20)

    _not_blank_title = validator("title", allow_reuse=True)(not_blank)
    _not_blank_instructions = validator("instructions", allow_reuse=True)(not_blank)

    @validator("type")
    def validate_type(cls, v):
        v = v.strip().lower()
        if v not in CHALLENGE_TYPES:
            raise ValueError(f"Invalid challenge type: {v}")
        return v

class AIGenerateDailyContentResponse(BaseModel):
    wordSuggestions: List[WordSuggestion]
    challengeSuggestions: List[ChallengeSuggestion]
    meta: Dict

class WordOfDayInput(BaseModel):
    word: str = Field(..., max_length=50)
    meaning: str = Field(..., max_length=300)
    example: str = Field(..., max_length=300)
    pronunciation: Optional[str] = Field(None, max_length=100)

    _not_blank_word = validator("word", allow_reuse=True)(not_blank)
    _not_blank_meaning = validator("meaning", allow_reuse=True)(not_blank)
    _not_blank_example = validator("example", allow_reuse=True)(not_blank)

class ChallengeInput(BaseModel):
    title: str = Field(..., max_length=120)
    type: str = Field(...)
    instructions: str = Field(..., max_length=1000)
    estimatedMinutes: int = Field(..., ge=1, le=15)

    _not_blank_title = validator("title", allow_reuse=True)(not_blank)
    _not_blank_instructions = validator("instructions", allow_reuse=True)(not_blank)

    @validator("type")
    def validate_type(cls, v):
        v = v.strip().lower()
        if v not in CHALLENGE_TYPES:
            raise ValueError(f"Invalid challenge type: {v}")
        return v

class SaveDraftRequest(BaseModel):
    classId: str
    gradeLevel: str
    contentDate: date
    sourceType: str = Field(..., regex="^(manual|ai_assisted)$")
    wordOfDay: WordOfDayInput
    challenge: ChallengeInput

    @validator("classId", "gradeLevel", pre=True)
    def validate_not_blank(cls, v):
        return not_blank(v)

class SaveDraftResponse(BaseModel):
    id: str
    status: str
    message: str

class PublishRequest(BaseModel):
    draftId: str

class PublishResponse(BaseModel):
    id: str
    status: str
    publishedAt: datetime
    message: str

class StudentDailyContentResponse(BaseModel):
    contentDate: date
    classId: str
    wordOfDay: WordOfDayInput
    challenge: ChallengeInput
    teacher: Dict
    status: str
