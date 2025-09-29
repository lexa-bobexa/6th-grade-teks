from fractions import Fraction
from typing import Any, Dict, Tuple

import sympy as sp


def eval_compute(template: Dict[str, Any], params: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
    """Evaluate the template's compute expression using params.

    This is a minimal, safe evaluator that supports known forms from the spec.
    Returns (answer, meta_dict).
    """
    compute = template.get("compute", "").strip()
    item_type = template.get("type")
    meta: Dict[str, Any] = {"type": item_type}

    # Trapezoid area
    if "(b1 + b2)/2 * h" in compute or compute == "A = (b1 + b2)/2 * h":
        b1 = int(params["b1"]) if "b1" in params else int(params.get("b1_min", 0))
        b2 = int(params["b2"]) if "b2" in params else int(params.get("b2_min", 0))
        h = int(params["h"]) if "h" in params else int(params.get("h_min", 0))
        ans = area_trapezoid(b1, b2, h)
        meta.update({"b1": b1, "b2": b2, "h": h})
        return ans, meta

    # Unit rate
    if compute.startswith("unit = ") and "/" in compute:
        x = params.get("x")
        y = params.get("y")
        if x is None or y is None:
            raise ValueError("Missing x or y for unit rate")
        return unit_rate(x, y), meta

    # One-step equation (placeholder: delegate to solve_one_step_equation)
    if "solve for x" in compute:
        form = params.get("form")
        a = params.get("a")
        b = params.get("b")
        c = params.get("c")
        d = params.get("d")
        return solve_one_step_equation(form, a, b, c, d), meta

    # Generic op apply for rationals ops
    if compute.startswith("result = op_apply"):
        a = params.get("a")
        b = params.get("b")
        op = params.get("op")
        if op not in {"+", "-", "×", "÷"}:
            raise ValueError("Unsupported op")
        return _op_apply(a, b, op), meta

    raise NotImplementedError(f"Unsupported compute expression: {compute}")


def solve_one_step_equation(form: str | None, a: Any, b: Any, c: Any, d: Any) -> Fraction:
    """Solve simple one-step equations for x.

    Supported forms: 'x + a = b', 'x - a = b', 'c x = d', 'x / c = d'
    Coefficients may be ints or Fractions (as strings like '-7/2').
    """
    def to_fraction(val: Any) -> Fraction:
        if isinstance(val, Fraction):
            return val
        if isinstance(val, int):
            return Fraction(val, 1)
        if isinstance(val, float):
            return Fraction(val).limit_denominator()
        if isinstance(val, str) and "/" in val:
            return Fraction(val)
        return Fraction(int(val), 1)

    if not form:
        raise ValueError("Equation form required")

    if form == "x + a = b":
        a_f, b_f = to_fraction(a), to_fraction(b)
        return b_f - a_f
    if form == "x - a = b":
        a_f, b_f = to_fraction(a), to_fraction(b)
        return b_f + a_f
    if form == "c x = d":
        c_f, d_f = to_fraction(c), to_fraction(d)
        if c_f == 0:
            raise ZeroDivisionError("c cannot be zero")
        return d_f / c_f
    if form == "x / c = d":
        c_f, d_f = to_fraction(c), to_fraction(d)
        return c_f * d_f

    raise NotImplementedError(f"Unsupported form: {form}")


def area_trapezoid(b1: int, b2: int, h: int) -> int:
    if b1 <= 0 or b2 <= 0 or h <= 0:
        raise ValueError("b1, b2, h must be positive")
    return int((b1 + b2) * h / 2)


def unit_rate(x: float | int, y: float | int) -> float:
    x_val = float(x)
    y_val = float(y)
    if x_val == 0.0:
        raise ZeroDivisionError("x cannot be zero for unit rate")
    return y_val / x_val


def equiv_expr(lhs: str, rhs: str) -> bool:
    x, y, z = sp.symbols("x y z")
    try:
        lhs_s = sp.simplify(sp.sympify(lhs))
        rhs_s = sp.simplify(sp.sympify(rhs))
        return sp.simplify(lhs_s - rhs_s) == 0
    except Exception:
        return False


def _op_apply(a: Any, b: Any, op: str) -> float:
    a_v = float(a)
    b_v = float(b)
    if op == "+":
        return a_v + b_v
    if op == "-":
        return a_v - b_v
    if op == "×":
        return a_v * b_v
    if op == "÷":
        if b_v == 0.0:
            raise ZeroDivisionError("division by zero")
        return a_v / b_v
    raise ValueError("Unknown operator")
