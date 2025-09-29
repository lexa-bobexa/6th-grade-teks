"""Tests for the solver engine."""

import pytest
from engines.solver import (
    area_trapezoid, unit_rate, solve_one_step_equation, 
    equiv_expr, eval_compute
)


def test_area_trapezoid():
    """Test trapezoid area calculation."""
    assert area_trapezoid(7, 13, 4) == 40
    assert area_trapezoid(5, 10, 6) == 45
    assert area_trapezoid(3, 9, 2) == 12


def test_area_trapezoid_validation():
    """Test trapezoid area validation."""
    with pytest.raises(ValueError):
        area_trapezoid(0, 5, 3)
    with pytest.raises(ValueError):
        area_trapezoid(5, -2, 3)
    with pytest.raises(ValueError):
        area_trapezoid(5, 2, 0)


def test_unit_rate():
    """Test unit rate calculation."""
    assert unit_rate(2, 10) == 5.0
    assert unit_rate(3, 15) == 5.0
    assert unit_rate(4, 20) == 5.0


def test_unit_rate_validation():
    """Test unit rate validation."""
    with pytest.raises(ZeroDivisionError):
        unit_rate(0, 10)


def test_solve_one_step_equation():
    """Test one-step equation solving."""
    from fractions import Fraction
    
    # x + 3 = 7
    assert solve_one_step_equation("x + a = b", 3, 7, None, None) == 4
    
    # x - 2 = 5
    assert solve_one_step_equation("x - a = b", 2, 5, None, None) == 7
    
    # 3x = 15
    assert solve_one_step_equation("c x = d", 3, 15, None, None) == 5
    
    # x/4 = 3
    assert solve_one_step_equation("x / c = d", 4, 3, None, None) == 12


def test_equiv_expr():
    """Test expression equivalence."""
    assert equiv_expr("x + 1", "1 + x") == True
    assert equiv_expr("2*x", "x*2") == True
    assert equiv_expr("x + 1", "x + 2") == False


def test_eval_compute_trapezoid():
    """Test template evaluation for trapezoid."""
    template = {
        "teks": "6.8B",
        "type": "numeric",
        "compute": "A = (b1 + b2)/2 * h"
    }
    params = {"b1": 6, "b2": 10, "h": 4}
    
    answer, meta = eval_compute(template, params)
    assert answer == 32
    assert meta["type"] == "numeric"


def test_eval_compute_unit_rate():
    """Test template evaluation for unit rate."""
    template = {
        "teks": "6.4",
        "type": "numeric", 
        "compute": "unit = y/x"
    }
    params = {"x": 3, "y": 12}
    
    answer, meta = eval_compute(template, params)
    assert answer == 4.0
    assert meta["type"] == "numeric"
