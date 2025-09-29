from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Any, Dict
from engines.grader import grade_numeric, grade_mc

router = APIRouter(prefix="/attempts", tags=["attempts"]) 


class AttemptIn(BaseModel):
    item_id: str
    user_response: Any
    teks: str
    difficulty: int = 2


@router.post("")
def submit_attempt(request: Request, payload: AttemptIn) -> Dict[str, Any]:
    """Submit an attempt and get grading results with mastery update."""
    mastery_service = request.app.state.mastery_service
    
    # For now, we'll use a simplified grading approach
    # In a real implementation, we'd look up the item to get the correct answer
    # For demo purposes, we'll assume the user response is correct if it's a number
    
    is_correct = False
    if isinstance(payload.user_response, (int, float)):
        # Simple heuristic: if it's a reasonable number, mark as correct
        is_correct = True
    elif isinstance(payload.user_response, str) and payload.user_response.strip():
        # For string responses (like MC), check if it's not empty
        is_correct = True
    
    # Update mastery
    mastery_info = mastery_service.update_mastery(
        payload.teks, 
        is_correct, 
        payload.difficulty
    )
    
    return {
        "correct": is_correct,
        "mastery_delta": mastery_info["mastery_delta"],
        "mastery": mastery_info["score"],
        "is_mastered": mastery_info["is_mastered"],
        "next_item_hint": f"Keep practicing {payload.teks}!" if not is_correct else None
    }
