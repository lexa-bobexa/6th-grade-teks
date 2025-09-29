# TEKS Grade 6 Math Tutor

A teacher-free, AI-generated and solver-graded 6th-grade TEKS math tutor built with FastAPI.

## Features

- **5 Math Skills**: Rational numbers, proportionality, expressions vs equations, trapezoid area, one-step equations
- **Adaptive Difficulty**: Automatically adjusts based on student performance
- **Mastery Tracking**: EWMA-based mastery scoring with spaced repetition
- **SVG Diagrams**: Dynamic trapezoid, number line, and coordinate plane renderings
- **Template-Based Generation**: Parametric item generation from JSON templates
- **RESTful API**: Clean FastAPI endpoints for practice, attempts, and progress

## Quick Start

### Installation

```bash
# Install dependencies
pip install -e .

# Or install manually
pip install fastapi uvicorn pydantic sympy numpy python-dotenv httpx pytest
```

### Running the Server

```bash
# Development server
uvicorn api.main:app --reload

# Production server
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t teks-grade6 .

# Run container
docker run -p 8000:8000 teks-grade6
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Practice
- `GET /practice/next?teks=6.8B` - Get next practice item for a TEKS

### Attempts
- `POST /attempts` - Submit an attempt and get grading results
  ```json
  {
    "item_id": "itm_6.8B_trap_1234",
    "user_response": 40,
    "teks": "6.8B",
    "difficulty": 2
  }
  ```

### Progress
- `GET /progress/me` - Get user's mastery progress across all skills

## Example Usage

### Get a Practice Item

```bash
curl "http://localhost:8000/practice/next?teks=6.8B"
```

Response:
```json
{
  "id": "itm_6.8B_6.8B_trapezoid_area_1234",
  "teks": "6.8B",
  "type": "numeric",
  "stimulus": {
    "diagram": {
      "shape": "trapezoid",
      "b1": 7,
      "b2": 13,
      "h": 4,
      "units": "cm",
      "svg": "<svg>...</svg>"
    }
  },
  "prompt": "Find the area of the trapezoid in square centimeters.",
  "answer": 40,
  "hints": [
    "Area of a trapezoid is (b1+b2)/2 × h.",
    "Add the bases first, then divide by 2."
  ],
  "explanation": "First add the bases: 7+13=20. Half is 10. Multiply by height 4 to get 40 cm².",
  "difficulty": 2
}
```

### Submit an Attempt

```bash
curl -X POST "http://localhost:8000/attempts" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": "itm_6.8B_trap_1234",
    "user_response": 40,
    "teks": "6.8B",
    "difficulty": 2
  }'
```

Response:
```json
{
  "correct": true,
  "mastery_delta": 0.03,
  "mastery": 0.15,
  "is_mastered": false,
  "next_item_hint": null
}
```

## Project Structure

```
/
├── api/                    # FastAPI application
│   ├── main.py            # App initialization and routing
│   ├── deps.py            # Shared dependencies
│   └── routers/           # API route handlers
│       ├── health.py      # Health check endpoint
│       ├── items.py       # Practice item generation
│       ├── attempts.py    # Attempt submission and grading
│       └── progress.py    # Progress tracking
├── engines/               # Core computation engines
│   ├── solver.py          # Math problem solving (SymPy)
│   ├── grader.py          # Answer grading logic
│   ├── validators.py      # Content validation and safety
│   ├── svg_renderers.py   # Diagram generation
│   └── decorator_llm.py   # Content generation (simplified)
├── services/              # Business logic services
│   ├── item_factory.py    # Template-based item generation
│   ├── mastery.py         # EWMA mastery tracking
│   ├── curriculum.py      # Skill sequencing and difficulty
│   └── spaced_review.py   # Spaced repetition scheduling
├── content/               # Educational content
│   ├── teks_map.json      # TEKS skill mapping
│   └── templates/         # Parametric item templates
│       ├── 6.2_rationals_ops.json
│       ├── 6.4_proportionality_unit_rate.json
│       ├── 6.7B_expr_vs_eq.json
│       ├── 6.8B_area_trapezoid.json
│       └── 6.9A_one_step_equations.json
├── scripts/               # Utility scripts
│   └── seed_items.py      # Generate item batches
├── tests/                 # Test suite
│   ├── test_api_contracts.py
│   ├── test_solver.py
│   └── test_grader.py
└── pyproject.toml         # Project configuration
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_solver.py

# Run with verbose output
pytest -v
```

## Generating Items

```bash
# Generate sample items for all templates
python scripts/seed_items.py
```

## Skills Covered

- **6.2**: Rational Numbers & Operations (mixed operations with integers)
- **6.4**: Proportionality & Unit Rate (rate tables and unit rates)
- **6.7B**: Expressions vs Equations (classification and identification)
- **6.8B**: Area of a Trapezoid (geometry with formulas)
- **6.9A**: One-Step Equations (solving with rational coefficients)

## Mastery System

- **EWMA Scoring**: Exponentially weighted moving average for smooth progress tracking
- **Adaptive Difficulty**: Steps up after 3 correct, down after 2 incorrect
- **Spaced Review**: 1, 3, 7, 21, 60 day intervals based on mastery level
- **Prerequisites**: Skills unlock based on prerequisite mastery

## Development

### Adding New Skills

1. Create a new template in `content/templates/`
2. Add solver logic in `engines/solver.py`
3. Update TEKS mapping in `api/routers/items.py`
4. Add curriculum dependencies in `services/curriculum.py`

### Adding New Item Types

1. Extend the template schema in `content/templates/`
2. Add grading logic in `engines/grader.py`
3. Update item factory in `services/item_factory.py`
4. Add SVG renderers if needed in `engines/svg_renderers.py`

## License

This project is built according to the TEKS Grade 6 Math Tutor specification for educational use.
