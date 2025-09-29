from fastapi import APIRouter, Query, Request
from typing import Any, Dict
import random

router = APIRouter(prefix="/practice", tags=["practice"]) 

@router.get("/next")
def get_next_item(request: Request, teks: str = Query(..., alias="teks")) -> Dict[str, Any]:
    """Get the next practice item for a given TEKS."""
    item_factory = request.app.state.item_factory
    curriculum_service = request.app.state.curriculum_service
    
    # Map TEKS to template IDs
    teks_to_template = {
        "6.2": "6.2_rationals_ops",
        "6.4": "6.4_unit_rate", 
        "6.7B": "6.7B_expr_vs_eq",
        "6.8B": "6.8B_trapezoid_area",
        "6.9A": "6.9A_one_step"
    }
    
    template_id = teks_to_template.get(teks, "6.8B_trapezoid_area")
    
    # Generate item with random seed
    seed = random.randint(1000, 9999)
    item = item_factory.generate_item(template_id, seed)
    
    return item
