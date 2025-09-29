# TEKS Grade 6 Math Tutor

A teacher-free, AI-generated and solver-graded 6th-grade TEKS math tutor with a modern React frontend and FastAPI backend.

## 🎯 Features

### Backend (FastAPI)
- ✅ **5 Math Skills**: Rational numbers, proportionality, expressions vs equations, trapezoid area, one-step equations
- ✅ **Adaptive Difficulty**: Automatically adjusts based on student performance
- ✅ **Mastery Tracking**: EWMA-based mastery scoring with spaced repetition
- ✅ **SVG Diagrams**: Dynamic trapezoid, number line, and coordinate plane renderings
- ✅ **Template-Based Generation**: Parametric item generation from JSON templates
- ✅ **RESTful API**: Clean FastAPI endpoints for practice, attempts, and progress

### Frontend (React + TypeScript)
- ✅ **Modern Dark UI**: Sleek dark theme with smooth animations
- ✅ **Item Player**: Supports numeric and multiple-choice questions
- ✅ **MathJax Integration**: Beautiful LaTeX math rendering
- ✅ **TEKS Map**: Visual skill grid with mastery rings
- ✅ **Progress Dashboard**: Track attempts, mastery, and skill growth
- ✅ **Review Builder**: Spaced repetition with custom practice sets
- ✅ **Accessibility**: Dyslexia-friendly fonts, text size controls, high contrast theme
- ✅ **Offline-First**: Persisted state with IndexedDB/localStorage
- ✅ **Responsive**: Mobile-first design with adaptive navigation

## 📦 Project Structure

```
6th-grade-teks/
├── api/                    # FastAPI backend
│   ├── main.py            # App entry point
│   ├── deps.py            # Dependency injection
│   └── routers/           # API endpoints
├── engines/               # Core logic
│   ├── solver.py          # Symbolic math solver
│   ├── grader.py          # Answer validation
│   └── svg_renderers.py   # Dynamic diagrams
├── services/              # Business logic
│   ├── item_factory.py    # Item generation
│   ├── mastery.py         # Mastery scoring
│   └── spaced_review.py   # Review scheduling
├── content/               # TEKS templates
│   ├── teks_map.json
│   └── templates/
├── frontend/              # React app
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── state/         # Zustand stores
│   │   ├── services/      # API client
│   │   └── App.tsx
│   ├── index.html
│   └── package.json
└── tests/                 # Unit tests
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Install Python dependencies
pip install -e .

# Or manually
pip install fastapi uvicorn pydantic sympy numpy python-dotenv httpx pytest

# Run development server
uvicorn api.main:app --reload --port 8000

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# App runs at http://localhost:5173
```

### Docker Deployment

```bash
# Build image
docker build -t teks-grade6 .

# Run container
docker run -p 8000:8000 teks-grade6
```

## 🔌 API Endpoints

### Health Check
- `GET /health` - Service health status

### Practice
- `GET /practice/next?teks_code=6.7B&difficulty=3` - Get next practice item
- `POST /practice/retry/{item_id}` - Retry an item with different values

### Attempts
- `POST /attempts` - Submit an attempt
  ```json
  {
    "item_id": "abc123",
    "user_id": "student_1",
    "response": 42,
    "time_ms": 15000
  }
  ```

### Progress
- `GET /progress/{user_id}` - Get user's mastery progress

### Items
- `GET /items/{item_id}` - Get specific item details

## 🎨 Frontend Architecture

### State Management (Zustand)
- **Auth**: User sign-in/sign-out
- **Settings**: Theme, accessibility, preferences
- **Mastery**: Skill-level scores and review dates
- **Practice**: Current item, results, queue

### Key Components
- `ItemPlayer` - Main practice interface with hint modal
- `SkillTile` - TEKS skill card with mastery ring
- `MathText` - MathJax wrapper for LaTeX rendering
- `HintModal` - Progressive hint system
- `MasteryBar` - Visual progress indicator

### Routing
- `/signin` - User authentication
- `/` - TEKS skill map (Home)
- `/practice` - Item player
- `/review` - Spaced repetition builder
- `/progress` - Analytics dashboard
- `/settings` - Accessibility & preferences

## 🧪 Testing

```bash
# Run backend tests
pytest tests/ -v

# Run frontend tests (when added)
cd frontend && npm test
```

## 📝 Content Templates

Each TEKS standard has a JSON template:

```json
{
  "id": "6.7B",
  "title": "Expressions vs Equations",
  "type": "numeric",
  "difficulty_range": [1, 5],
  "prompt_template": "Solve for x: {lhs} = {rhs}",
  "variables": {
    "lhs": {"type": "expression", "complexity": 2},
    "rhs": {"type": "int", "range": [1, 20]}
  }
}
```

## 🎯 Mastery Algorithm

Uses Exponential Weighted Moving Average (EWMA):
- **Correct answer**: +3% mastery
- **Incorrect answer**: -1% mastery
- **Review scheduling**: Items due 7 days after practice
- **Spaced repetition**: Adaptive review intervals

## 🛠️ Tech Stack

**Backend:**
- FastAPI (async Python web framework)
- SymPy (symbolic mathematics)
- Pydantic (data validation)
- NumPy (numerical computations)

**Frontend:**
- React 19 + TypeScript
- Vite (build tool)
- Zustand (state management)
- Tailwind CSS
- MathJax (LaTeX rendering)
- Radix UI (accessible components)

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

- [API Specification](v1spec.md) - Backend API contracts
- [Frontend UI/UX Spec](frontend-ui-ux-spec.md) - Design system and user flows

## 🎓 TEKS Standards Covered

- **6.2**: Rational Numbers & Operations
- **6.4**: Proportionality & Unit Rate
- **6.7B**: Distinguish expressions from equations
- **6.8B**: Model and solve area of trapezoids
- **6.9A**: Write one-step equations

## 🚧 Roadmap

- [ ] Add expression input type (symbolic math)
- [ ] Plot/graph input for coordinate geometry
- [ ] Teacher dashboard with class analytics
- [ ] Export progress reports (PDF)
- [ ] More TEKS standards (6.3, 6.5, 6.10+)
- [ ] Parent view with progress tracking
- [ ] Voice read-aloud for accessibility
- [ ] Printable worksheet generator

---

Built with ❤️ for middle school math learners