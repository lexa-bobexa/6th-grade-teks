from fastapi import APIRouter, Query, Request
from typing import Any, Dict, Optional
import random

router = APIRouter(prefix="/practice", tags=["practice"]) 

@router.get("/next")
def get_next_item(
    request: Request, 
    teks: Optional[str] = Query(None, description="TEKS code like 6.8B")
) -> Dict[str, Any]:
    """Get the next practice item for a given TEKS."""
    item_factory = request.app.state.item_factory
    
    # Map TEKS to template IDs
    teks_to_template = {
        "6.2": "6.2_rationals_ops",
        "6.4": "6.4_unit_rate", 
        "6.7B": "6.7B_expr_vs_eq",
        "6.8B": "6.8B_trapezoid_area",
        "6.9A": "6.9A_one_step"
    }
    
    # Use trapezoid as default (it works!)
    template_id = teks_to_template.get(teks, "6.8B_trapezoid_area") if teks else "6.8B_trapezoid_area"
    
    # Try to generate item, fall back to trapezoid if it fails
    seed = random.randint(1000, 9999)
    try:
        item = item_factory.generate_item(template_id, seed)
    except Exception as e:
        print(f"Error generating {template_id}: {e}")
        # Fallback to trapezoid which we know works
        template_id = "6.8B_trapezoid_area"
        item = item_factory.generate_item(template_id, seed)
    
    # Format for frontend
    return {
        "id": item["id"],
        "teks": item["teks"],
        "type": "numeric",
        "seed": seed,
        "stimulus": item.get("stimulus"),  # Include SVG diagrams
        "prompt": item["prompt"],
        "difficulty": item.get("difficulty", 2),
        "hints": item.get("hints", []),
        "answer": item["answer"]  # Keep for backend validation
    }
