"""
Prompt builder for AI daily content generation
"""
from app.schemas.daily_content import AIGenerateDailyContentRequest
from datetime import date

def build_daily_content_generation_prompt(request: AIGenerateDailyContentRequest) -> str:
    """
    Build a system/user prompt for the LLM to generate daily content suggestions.
    """
    system = (
        "You are generating classroom-safe daily learning content suggestions for teachers.\n"
        "Return JSON only. No markdown. No commentary.\n"
        "The response must strictly match the requested schema.\n"
        "Content must be age-appropriate, school-safe, non-political, non-sensitive, and suitable for children.\n"
        "Do not include unsafe, controversial, medical, religious, sexual, violent, or emotionally manipulative content."
    )
    user = f"""
Generate {request.countPerType} Word of the Day suggestions and {request.countPerType} Daily Challenge suggestions for:
- Grade Level: {request.gradeLevel}
- Age Group: {request.studentAgeGroup or ''}
- Subject: {request.subject or ''}
- Theme: {request.theme or ''}
- Content Date: {request.contentDate}
- Teacher Instructions: {request.teacherInstructions or ''}
- Allowed Challenge Types: {', '.join(request.challengeTypes)}

Rules:
- vocabulary must be easy to understand for the specified grade
- meaning must be short and simple
- example sentence must be child-friendly
- challenge estimatedMinutes must be between 1 and 5 unless strong teacher instructions imply otherwise
- challenge types must come only from the allowed list
- no duplicates
- output strict JSON only

Return exactly this JSON structure:
{{
  "wordSuggestions": [{{"word": "...", "meaning": "...", "example": "...", "pronunciation": "...", "difficulty": "easy"}}],
  "challengeSuggestions": [{{"title": "...", "type": "writing", "instructions": "...", "estimatedMinutes": 3, "difficulty": "easy"}}]
}}
"""
    return f"SYSTEM INSTRUCTION:\n{system}\n\nUSER INSTRUCTION:\n{user}"
