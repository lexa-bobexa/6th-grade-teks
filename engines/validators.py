from typing import Any, Iterable


BANNED_TERMS = {"kill", "weapon", "drugs", "alcohol"}


def moderate(texts: Iterable[str]) -> bool:
    for t in texts:
        low = t.lower()
        if any(term in low for term in BANNED_TERMS):
            return False
    return True


def check_trapezoid(params: dict[str, Any]) -> bool:
    try:
        b1 = int(params["b1"]) if "b1" in params else int(params.get("b1_min", 0))
        b2 = int(params["b2"]) if "b2" in params else int(params.get("b2_min", 0))
        h = int(params["h"]) if "h" in params else int(params.get("h_min", 0))
        return b1 > 0 and b2 > 0 and h > 0
    except Exception:
        return False


def check_distractors(correct: Any, distractors: list[Any], fn_list: list) -> bool:
    if any(d == correct for d in distractors):
        return False
    if len(set(map(str, distractors))) != len(distractors):
        return False
    for fn in fn_list or []:
        if not fn():
            return False
    return True
