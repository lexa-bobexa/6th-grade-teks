"""Tests for the grader engine."""

import pytest
from engines.grader import grade_numeric, grade_expression, grade_mc, grade_plot


def test_grade_numeric_exact():
    """Test exact numeric grading."""
    result = grade_numeric(42, 42, 0, "int", None)
    assert result["correct"] == True
    assert result["canonical"] == 42
    assert result["feedback_code"] == "OK"


def test_grade_numeric_with_tolerance():
    """Test numeric grading with tolerance."""
    result = grade_numeric(42.1, 42, 0.2, "decimal", None)
    assert result["correct"] == True
    assert result["canonical"] == 42


def test_grade_numeric_fraction():
    """Test fraction grading."""
    from fractions import Fraction
    result = grade_numeric(Fraction(1, 2), Fraction(1, 2), 0, "fraction", None)
    assert result["correct"] == True


def test_grade_numeric_incorrect():
    """Test incorrect numeric grading."""
    result = grade_numeric(41, 42, 0, "int", None)
    assert result["correct"] == False
    assert result["feedback_code"] == "NUM_MISMATCH"


def test_grade_numeric_parse_error():
    """Test parse error handling."""
    result = grade_numeric("not_a_number", 42, 0, "int", None)
    assert result["correct"] == False
    assert result["feedback_code"] == "PARSE_ERROR"


def test_grade_expression():
    """Test expression grading."""
    assert grade_expression("x + 1", "1 + x") == True
    assert grade_expression("2*x", "x*2") == True
    assert grade_expression("x + 1", "x + 2") == False


def test_grade_mc_correct():
    """Test correct multiple choice grading."""
    result = grade_mc("A", "A")
    assert result["correct"] == True
    assert result["canonical"] == "A"


def test_grade_mc_incorrect():
    """Test incorrect multiple choice grading."""
    result = grade_mc("B", "A")
    assert result["correct"] == False
    assert result["feedback_code"] == "MC_WRONG"


def test_grade_mc_multiple():
    """Test multiple choice with multiple selections."""
    result = grade_mc(["A", "B"], ["A", "B"])
    assert result["correct"] == True


def test_grade_plot_close():
    """Test plot grading with close points."""
    result = grade_plot((1.0, 2.0), (1.1, 2.1), 0.2)
    assert result["correct"] == True


def test_grade_plot_far():
    """Test plot grading with distant points."""
    result = grade_plot((1.0, 2.0), (3.0, 4.0), 0.2)
    assert result["correct"] == False
    assert result["feedback_code"] == "PLOT_OFF"
