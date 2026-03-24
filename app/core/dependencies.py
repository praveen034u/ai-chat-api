"""
Dependency Placeholders
"""
from fastapi import Depends, HTTPException, status

def get_current_teacher():
    """Dependency to get current teacher (placeholder)."""
    # TODO: Implement real authentication
    return {"teacher_id": "dummy-teacher-id"}

def get_current_student():
    """Dependency to get current student (placeholder)."""
    # TODO: Implement real authentication
    return {"student_id": "dummy-student-id"}
