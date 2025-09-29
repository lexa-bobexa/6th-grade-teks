from fractions import Fraction
from typing import Any, Dict

import sympy as sp


def grade_numeric(user_answer: Any, key: Any, tolerance: float, form: str, units: str | None = None) -> Dict[str, Any]:
    try:
        if form == "fraction":
            ua = Fraction(str(user_answer))
            kk = Fraction(str(key))
            correct = ua == kk
            canonical = str(kk)
        else:
            ua = float(user_answer)
            kk = float(key)
            correct = abs(ua - kk) <= (tolerance or 0)
            canonical = kk
        return {"correct": bool(correct), "canonical": canonical, "feedback_code": "OK" if correct else "NUM_MISMATCH"}
    except Exception:
        return {"correct": False, "canonical": key, "feedback_code": "PARSE_ERROR"}


def grade_expression(user_expr: str, key_expr: str) -> bool:
    try:
        return sp.simplify(sp.sympify(user_expr) - sp.sympify(key_expr)) == 0
    except Exception:
        return False


def grade_mc(choice: Any, correct_value: Any) -> Dict[str, Any]:
    correct = choice == correct_value or (isinstance(choice, list) and set(choice) == set(correct_value))
    return {"correct": bool(correct), "canonical": correct_value, "feedback_code": "OK" if correct else "MC_WRONG"}


def grade_plot(point: tuple[float, float], target: tuple[float, float], tol: float = 0.25) -> Dict[str, Any]:
    dx = float(point[0]) - float(target[0])
    dy = float(point[1]) - float(target[1])
    dist = (dx * dx + dy * dy) ** 0.5
    correct = dist <= tol
    return {"correct": bool(correct), "canonical": target, "feedback_code": "OK" if correct else "PLOT_OFF"}
