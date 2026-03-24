"""
Student Daily Content Router
"""
from fastapi import APIRouter, Depends
from app.schemas.daily_content import StudentDailyContentResponse
from app.core.dependencies import get_current_student

router = APIRouter(prefix="/student", tags=["Student Daily Content"])

@router.get("/daily-content", response_model=StudentDailyContentResponse)
async def get_daily_content(student=Depends(get_current_student)):
    """Get published daily content for students."""
    # Implementation will call daily_content_service.get_published_content
    pass
