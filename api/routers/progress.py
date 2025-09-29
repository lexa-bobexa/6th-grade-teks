from fastapi import APIRouter, Request
from typing import Dict, Any
from datetime import datetime

router = APIRouter(prefix="/progress", tags=["progress"]) 


@router.get("/me")
def get_progress_me(request: Request) -> Dict[str, Any]:
    """Get user's progress across all skills."""
    mastery_service = request.app.state.mastery_service
    
    # Get all mastery records
    all_mastery = mastery_service.get_all_mastery()
    
    # Convert to API format
    skills = []
    for record in all_mastery:
        skills.append({
            "teks": record.teks,
            "mastery": record.score,
            "last_seen": record.last_seen_at.isoformat() if record.last_seen_at else None,
            "due_review_at": record.due_review_at.isoformat() if record.due_review_at else None,
            "attempts": record.attempts,
            "level": mastery_service.get_mastery_level(record.teks)
        })
    
    # If no skills yet, return empty list
    if not skills:
        return {"skills": []}
    
    return {"skills": skills}
