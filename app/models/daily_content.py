"""
Daily Content Model (Supabase/Postgres)
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DailyContentDBModel(BaseModel):
    id: str
    title: str
    content: str
    class_id: str
    teacher_id: str
    date: datetime
    status: str  # e.g., 'draft', 'published'
    created_at: datetime
    updated_at: Optional[datetime]
