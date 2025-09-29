# TEKS 6th‑Grade Math Tutor – AI Item Generation & Grading Spec (v1)

This document contains concrete templates, prompts, validators, and API contracts to build a teacher‑free, AI‑generated + solver‑graded 6th‑grade TEKS math tutor.

---

## 0) Repository scaffold

```
/ (root)
  /api
    main.py
    deps.py
    routers/
      items.py
      attempts.py
      progress.py
      health.py
  /content
    teks_map.json
    templates/
      6.2_rationals_ops.json
      6.4_proportionality_unit_rate.json
      6.7B_expr_vs_eq.json
      6.8B_area_trapezoid.json
      6.9A_one_step_equations.json
  /engines
    solver.py           # SymPy wrappers, numeric utils
    grader.py           # numeric/expression/unit/plot graders
    decorator_llm.py    # prompts + schema validation
    validators.py       # content moderation + numeric/diagram guards
    svg_renderers.py    # trapezoid, number line, coordinate plane
  /services
    curriculum.py       # sequencing, unlock rules
    mastery.py          # EWMA/Elo-like per-skill mastery
    item_factory.py     # generate → decorate → validate → cache
    spaced_review.py    # review scheduler
  /web (optional Next.js app)
  /tests
    test_templates_fuzz.py
    test_grader_equivalence.py
    test_api_contracts.py
  /docs
    requirements.md
    spec_ai_generation.md
  /scripts
    seed_items.py
    nightly_regen.py
  .env.example
  pyproject.toml
  Dockerfile
```

---

## 1) Data contracts (JSON Schemas)

### 1.1 Template schema (parametric, pre-LLM)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ItemTemplate",
  "type": "object",
  "required": ["id", "teks", "type", "params", "compute", "presentation", "difficulty"],
  "properties": {
    "id": {"type": "string"},
    "teks": {"type": "string"},
    "type": {"enum": ["numeric", "mc", "expression", "plot", "drag"]},
    "difficulty": {"type": "integer", "minimum": 1, "maximum": 5},
    "params": {"type": "object"},
    "compute": {"type": "string", "description": "Pythonic expression to compute the answer from params."},
    "answer_format": {"type": "object", "properties": {"form": {"enum": ["int","fraction","decimal","mixed"]}, "tolerance": {"type": "number"}, "units": {"type": "string"}}},
    "presentation": {"type": "object"},
    "constraints": {"type": "object"}
  }
}
```

### 1.2 Live item schema (post-LLM decoration)

```json
{
  "id": "itm_6.8B_trap_3f92",
  "teks": "6.8B",
  "type": "numeric",
  "seed": 382914,
  "params": {"b1": 7, "b2": 13, "h": 4, "units": "cm"},
  "stimulus": {
    "diagram": {"shape": "trapezoid", "b1": 7, "b2": 13, "h": 4, "units": "cm"},
    "context": "A garden bed is shaped like a trapezoid..."
  },
  "prompt": "Find the area of the trapezoid in square centimeters.",
  "options": null,
  "answer": 40,
  "answer_equivalents": [40.0],
  "answer_format": {"form": "int", "tolerance": 0, "units": "cm^2"},
  "hints": ["Area of a trapezoid is (b1+b2)/2 × h.", "Add bases first, then divide by 2."],
  "explanation": "First add the bases: 7+13=20. Half is 10. Multiply by height 4 to get 40 cm².",
  "difficulty": 2,
  "tags": ["area","trapezoid","formulas"],
  "safety": {"moderation_passed": true}
}
```

---

## 2) Five parametric templates (MVP)

### 2.1 6.2 – Rational Numbers & Operations (mixed ops with integers)

`content/templates/6.2_rationals_ops.json`

```json
{
  "id": "6.2_rationals_ops",
  "teks": "6.2",
  "type": "numeric",
  "difficulty": 2,
  "params": {
    "a_min": -12, "a_max": 12,
    "b_min": -12, "b_max": 12,
    "op": ["+","-","×","÷"],
    "require_nontrivial": true
  },
  "compute": "result = op_apply(a,b,op)",
  "answer_format": {"form":"decimal","tolerance":0,"units":""},
  "presentation": {"ask":"Compute the value.", "diagram": null},
  "constraints": {"no_div_zero": true, "denom_divisibility": [2,4,5,10]}
}
```

### 2.2 6.4 – Proportionality (unit rate & rate tables)

`content/templates/6.4_proportionality_unit_rate.json`

```json
{
  "id": "6.4_unit_rate",
  "teks": "6.4",
  "type": "numeric",
  "difficulty": 2,
  "params": {"x": {"min": 2, "max": 12}, "y": {"min": 6, "max": 96}, "units_x": ["hours","miles","packs"], "units_y": ["miles","dollars","points"]},
  "compute": "unit = y/x",
  "answer_format": {"form":"decimal","tolerance":0.001},
  "presentation": {"ask":"Find the unit rate.", "diagram": null},
  "constraints": {"reasonable_unit_pairs": true}
}
```

### 2.3 6.7B – Distinguish Expressions vs. Equations

`content/templates/6.7B_expr_vs_eq.json`

```json
{
  "id": "6.7B_expr_vs_eq",
  "teks": "6.7B",
  "type": "mc",
  "difficulty": 2,
  "params": {"forms": ["4(x+3)", "(y-5)=12", "2^3+7", "k/5=3", "9m-4"]},
  "compute": "labels = classify_exprs(forms)",
  "answer_format": {"form":"label"},
  "presentation": {"ask":"Select all that are equations."},
  "constraints": {"at_least_two_each": true}
}
```

### 2.4 6.8B – Geometry: Area of a Trapezoid

`content/templates/6.8B_area_trapezoid.json`

```json
{
  "id": "6.8B_trapezoid_area",
  "teks": "6.8B",
  "type": "numeric",
  "difficulty": 2,
  "params": {"b1_min":4, "b1_max":14, "b2_min":6, "b2_max":18, "h_min":3, "h_max":9, "units":["cm","m"]},
  "compute": "A = (b1 + b2)/2 * h",
  "answer_format": {"form":"int","tolerance":0,"units":"u^2"},
  "presentation": {"diagram":"trapezoid_svg","ask":"Find the area."},
  "constraints": {"nondegenerate": true, "integer_area": true}
}
```

### 2.5 6.9A – One‑Step Equations with Rational Coefficients

`content/templates/6.9A_one_step_equations.json`

```json
{
  "id": "6.9A_one_step",
  "teks": "6.9A",
  "type": "numeric",
  "difficulty": 2,
  "params": {"form": ["x + a = b", "x - a = b", "c x = d", "x / c = d"], "a_min": -15, "a_max": 15, "b_min": -30, "b_max": 30, "c_choices": [2,3,4,5,6,8,10]},
  "compute": "solve for x",
  "answer_format": {"form":"fraction","tolerance":0},
  "presentation": {"ask":"Solve for x."},
  "constraints": {"clean_fraction_results": true}
}
```

---

## 3) LLM decorator prompts (system & user)

### 3.1 System prompt (decoration model)

```
You are an education content decorator. Input = a math item template with parameters and the computed correct answer.
Your job: (1) produce a SHORT school‑appropriate context sentence, (2) write the student‑facing prompt, (3) create 2–3 concise hints, (4) a one‑paragraph explanation, (5) if type is MC, generate 3 plausible distractors with rationales targeting common misconceptions.
Rules:
- Never change numbers or computed answer.
- Grade 6 reading level; no brand names, people names, locations, or mature topics.
- Keep contexts neutral and classroom‑safe.
- For geometry, reference the provided diagram but do NOT invent new measures.
- For units, use those given and include them in the prompt.
Output JSON ONLY matching schema: {"context","prompt","hints":[...],"explanation","distractors":[{"value":...,"why":...}]}
If MC: ensure exactly one correct option; distractors must be unique and not equal to the answer.
```

### 3.2 User prompt (filled by backend)

```
TEMPLATE:
{template_json}
PARAMS CHOSEN:
{params_json}
COMPUTED ANSWER:
{answer_json}
ITEM TYPE: {type}
Please decorate now.
```

### 3.3 Secondary cross‑check prompt (different model or seed)

```
Given this finished item JSON and the student prompt, recompute the answer independently.
Return: {"agree": true|false, "answer": <number|string>, "reason": "..."}
If disagree, explain briefly why.
```

---

## 4) Validators & guards

* **Moderation:** block if any banned term appears (wordlist), or if LLM output adds persons/places.
* **Numeric sanity:** template‑specific (e.g., trapezoid b1,b2,h > 0; integer area option respected; unit rate magnitudes reasonable).
* **Distractor checks:** all distinct; distance from correct value ≥ template‑specific threshold; match misconception generators.
* **Diagram guard:** trapezoid nondegenerate; triangle inequality checks when applicable; histogram bins > 0; coordinate plane points inside bounds.
* **Schema validation:** strict JSON schema pass before publish.

---

## 5) Engines (spec)

### 5.1 `engines/solver.py`

* `eval_compute(template, params) -> answer, meta`
* `solve_one_step_equation(form, a,b,c,d) -> Fraction`
* `area_trapezoid(b1,b2,h) -> int`
* `unit_rate(x,y) -> float`
* `equiv_expr(lhs, rhs) -> bool` (SymPy simplify)

### 5.2 `engines/grader.py`

* `grade_numeric(user_answer, key, tolerance, form, units)`
* `grade_expression(user_expr, key_expr) -> bool` (using SymPy)
* `grade_mc(choice, correct_value)`
* `grade_plot(point, target, tol=0.25)`
* Returns `{correct: bool, canonical: <rendered>, feedback_code: <enum>}`

### 5.3 `engines/validators.py`

* `moderate(texts) -> bool`
* `check_trapezoid(params) -> bool`
* `check_distractors(correct, distractors, fn_list)`

---

## 6) API contracts (FastAPI)

### `GET /practice/next?teks=6.8B`

* **200:** `{item}` (post‑LLM, validated)

### `POST /attempts`

* Req: `{item_id, user_response}`
* Res: `{correct, mastery_delta, next_item_hint?: string, mastery: number}`

### `GET /progress/me`

* Res: `{skills: [{teks, mastery, last_seen, due_review_at}]}`

### `POST /admin/templates/generate`

* Req: `{template_id, seed_count}` → pre‑cache N items

---

## 7) Mastery engine (EWMA defaults)

* `alpha = 0.2`; `threshold = 0.83`; `min_items = 15`; last‑5 rule ≥ 4/5.
* Difficulty step‑up after 3 correct in a row; step‑down after 2 incorrect.
* Spaced review: 1, 3, 7, 21 days.

---

## 8) Placement test (cold start)

* 12 items spanning 6.2, 6.4, 6.7B, 6.8B, 6.9A, 6.12.
* Set initial mastery by strand using EWMA with higher alpha (0.4) for faster convergence.

---

## 9) Property‑based tests (examples)

### 9.1 Fuzz trapezoid area

* Random b1,b2,h within bounds → `grader` must accept only correct area; distractors differ; integer area when required.

### 9.2 One‑step equations

* Auto‑generate forms; verify solver result re‑substitutes into original.

### 9.3 MC classification (6.7B)

* Ensure at least two equations and two expressions appear; LLM distractors never equal answers.

---

## 10) Sample seeds (human‑readable)

### 10.1 6.8B Trapezoid

```
params: {b1: 7, b2: 13, h: 4, units: "cm"}
answer: 40
hints: ["Use (b1+b2)/2 × h", "Compute bases first"]
explanation: "(7+13)/2=10; 10×4=40 cm²"
```

### 10.2 6.9A One‑Step

```
form: "3x = 18" → x = 6
form: "x - (−4) = 9" → x = 5
form: "x/5 = −7/2" → x = −35/2
```

---

## 11) LLM cost control

* Pre‑generate 100–300 items/skill nightly; cache by difficulty.
* Reuse contexts with slot‑filled nouns (generic, school‑safe).

---

## 12) Accessibility & i18n

* MathJax with `aria-hidden` carefully managed.
* Optional Spanish prompts via translation step **post‑validation** (answer unchanged).

---

## 13) Build order (implementation guide)

1. Implement `solver.py` + unit tests.
2. Implement `grader.py` + unit tests.
3. Implement `validators.py`.
4. Hard‑code one template (6.8B) → end‑to‑end `/practice/next` → `/attempts`.
5. Add LLM decorator + cross‑check, then expand to four more templates.
6. Add mastery engine + placement test.
7. Add spaced review + offline PWA cache.

---

## 14) Example decorator outputs (abridged)

**6.4 Unit Rate**

```
context: "Ava runs 12 miles in 2 hours."
prompt: "What is the unit rate in miles per hour?"
hints: ["Divide total miles by hours.", "12 ÷ 2 = ?"]
explanation: "Unit rate is per 1 hour: 12/2 = 6 mph."
```

**6.7B Expressions vs Equations (MC)**

```
prompt: "Select all equations."
distractors (examples): ["4(x+3)", "2^3+7"], correct: ["(y-5)=12", "k/5=3"]
```

---

## 15) Security & safety checklist

* Strip PII; prohibit LLM from naming people/places; profanity filter.
* Strict schema validation; reject on cross‑check disagreement.
* Log all rejected generations for offline review.

---

## 16) Acceptance criteria (MVP)

* 5 skills live, each with ≥200 pre‑generated items across difficulties 1–3.
* 0 grading mismatches in 10k fuzzed attempts.
* Student can reach mastery in at least 3 skills without teacher interaction using hints/reteach.

---

**End of v1 Spec**
