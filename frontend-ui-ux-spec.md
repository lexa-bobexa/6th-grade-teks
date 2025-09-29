# TEKS Grade 6 Tutor – Frontend UI/UX Spec (Student‑First, Data‑Aware)

Audience: middle‑school students (primary), with optional parent view. This spec defines screens, interactions, copy tone, accessibility, state, and data persistence (online/offline) for a teacher‑free, AI‑generated and solver‑graded experience.

---

## 1) Design principles

* **Simple > flashy:** 1 primary action per screen; short sentences; friendly microcopy.
* **Confidence building:** visible progress, instant feedback, gentle retries.
* **Motion with purpose:** micro‑animations ≤ 250 ms to reinforce outcomes (correct/incorrect, mastery gains).
* **Accessible by default:** WCAG 2.1 AA, keyboard navigable, high-contrast theme option, dyslexia‑friendly font toggle (OpenDyslexic/Atkinson Hyperlegible).
* **Offline‑first:** PWA with cached practice and queued attempts.

---

## 2) Information architecture (IA)

* **Entry:** Sign in → Placement → Home (TEKS Map) → Practice → Review → Progress
* **Global nav (bottom for mobile / left for desktop):** Home, Practice, Review, Progress, Settings
* **Contextual nav:** In‑practice: Hint, Reteach, Another like this, Report issue

---

## 3) Screens & flows

### 3.1 Sign In / Create Profile

* **Fields:** First name, last initial (optional), grade (6), nickname (optional). OAuth optional.
* **States:** New user → Placement prompt; Returning user → resume last activity.
* **Copy tone:** “Hi! I’m your math practice buddy. We’ll start with a quick check so I can pick the right problems.”

### 3.2 Placement Quiz (10–12 items)

* **UI:** Full‑screen item card; light gray background; progress stepper (1/12); skip allowed 2×.
* **Controls:** Numeric keypad (mobile), answer box, Submit, I’m not sure.
* **Feedback:** Minimal; only “Got it!” or “Thanks!” (no correct/incorrect to avoid test anxiety). After finish → personalized starting map.

### 3.3 Home – TEKS Map (Skill Grid)

* **Layout:** Grid of skill tiles grouped by strands (6.2, 6.3, 6.4–6.5, 6.7, 6.8, 6.9–6.10, 6.11, 6.12).
* **Tile content:** TEKS code, short title, mastery ring (0–100%), next‑due badge for spaced review.
* **Actions:** Tap tile → Practice; long‑press/ellipsis → Add to Review, View examples.
* **Filter:** “Ready to practice”, “Needs review”, “Mastered”.

### 3.4 Practice – Item Player

* **Header:** TEKS code + short title; mastery bar (thin, animated); difficulty chip (1–5).
* **Body:**

  * **Stimulus area:** MathJax expressions; dynamic SVG (e.g., trapezoid); alt text for diagrams.
  * **Prompt:** One or two short sentences; units emphasized.
  * **Answer input:**

    * Numeric: keypad, fraction helper (a/b), mixed number toggle.
    * MC: large pill buttons; allow multi‑select where applicable.
    * Expression: math input with simple symbols (× ÷ ^).
    * Plot: coordinate plane with snap‑to‑grid and keyboard arrow move.
  * **Tools row:** Hint, Reteach, Another like this, Report issue.
* **Footer:** Primary button (Submit → Next); timer (subtle, not punitive).
* **Feedback states:**

  * **Correct:** bounce tick + green glow around answer; toast “Nice! Mastery +3%”.
  * **Incorrect (1st time):** shake + message with targeted nudge; offer Hint.
  * **Incorrect (2nd time):** auto‑open scaffolded version; keep prior work ghosted.

### 3.5 Hint Modal

* **Up to 3 steps**; each reveals sequentially.
* “Show me a worked example” button opens a collapsible solution card.

### 3.6 Micro‑Reteach Card

* 3–5 bullet refresher (definition, formula, example, common pitfall). Appears inline between items when triggered.

### 3.7 Review Mode (Spiral & Test Prep)

* **Tabs:** Due Today, This Week, Custom Set.
* **Custom Set flow:** choose skills → item count (10/20/30) → start; includes printable PDF option.

### 3.8 Progress

* **Overview:** mastery by strand (donut charts), streaks, time‑on‑task, items practiced.
* **Detail:** skill‑level history graph (mastery vs time), typical errors (chips with example and quick reteach link).

### 3.9 Settings

* **Accessibility:** dyslexia font toggle, text size (S/M/L), color theme (default/high contrast), read‑aloud.
* **Answer preferences:** fractions vs decimals, require units (on/off).
* **Privacy:** export data (JSON), clear device data, sign out.

### 3.10 Error/Offline states

* **Offline:** banner “You’re practicing offline. We’ll sync when you’re back.”
* **Sync conflict:** keep both; last‑write‑wins on attempts, merge mastery using server reconciliation.

---

## 4) Component library (React)

* **Atoms:** Button, IconButton, Input, NumericKeypad, Toggle, Chip, Tag, ProgressBar, Tooltip, Toast, Modal.
* **Molecules:** ItemCard, MasteryRing, SkillTile, HintSteps, ReteachCard, CoordinatePlane, NumberLine, FractionInput, MixedNumberInput, UnitBadge.
* **Organisms:** ItemPlayer, TEKSMap, ReviewBuilder, ProgressOverview, PlacementStepper.

---

## 5) Copy & micro‑interactions (examples)

* **Submit success:** “Nice work!” / “You’re getting the hang of this.”
* **Submit fail (first):** “Close! Try the hint?”
* **Submit fail (second):** “Let’s break it down together.”
* **Mastery up:** “+3% in 6.8B • Area of trapezoids.”
* **Streaks:** flame icon with count; reset message is gentle (no shaming).

---

## 6) Accessibility details

* Full keyboard path for every input type; visible focus rings.
* MathJax with `aria-label` equivalents; diagrams expose alt text and data (b1,b2,h).
* Color is not the only signal (icons + text); success/error motion respects `prefers-reduced-motion`.

---

## 7) Frontend state model

```
appState = {
  auth: { userId, displayName, lastSeenAt },
  connectivity: { online: true|false, lastSyncAt },
  katalog: { skills[], templatesIndex },
  practice: {
    currentItem: {id, teks, seed, prompt, stimulus, type, answer_format, hints, difficulty},
    lastResult: {correct, feedbackCode, masteryDelta},
    queue: [itemIds],
    timerMs,
  },
  mastery: { [teksCode]: {score: 0..1, attempts, lastSeenAt, dueReviewAt} },
  review: { selectedSkills[], setSize },
  settings: { theme, fontSize, dyslexiaFont, readAloud, unitPrefs },
  analyticsBuffer: [{event, ts, payload}],
}
```

---

## 8) Data persistence & syncing

### 8.1 Local (offline)

* **Storage:** IndexedDB (Dexie) for items, attempts, mastery, settings; Cache Storage for assets/SVGs; localStorage only for small flags.
* **Schema (IndexedDB):**

```
db.items:      {id PK, teks, seed, payloadJSON, createdAt}
db.attempts:   {id PK, itemId, userId, correct, responseJSON, timeMs, ts}
db.mastery:    {userId+teks PK, score, attempts, lastSeenAt, dueReviewAt}
db.settings:   {id="me", theme, fontSize, dyslexiaFont, unitPrefs}
db.queues:     {name PK, items[]}
db.analytics:  {id PK, event, payloadJSON, ts, synced: bool}
```

* **Queueing:** attempts and analytics events appended locally; background sync via Service Worker when online.

### 8.2 Server sync

* **Endpoints used:** `/practice/next`, `/attempts`, `/progress/me`.
* **Strategy:**

  * On app start and every 10 min: pull TEKS map & due reviews; push unsynced attempts in order; resolve conflicts by server recomputing mastery.
  * If item payload exists locally and server version hash differs → keep both; prefer server for grading metadata.

---

## 9) Analytics (student‑friendly, privacy‑safe)

* **Events:** `app_open`, `placement_start`, `placement_finish`, `practice_start`, `item_served`, `attempt_submit`, `attempt_result`, `hint_open`, `reteach_open`, `review_start`, `review_finish`, `settings_change`, `offline_start`, `offline_end`.
* **Payload (example `attempt_result`):** `{itemId, teks, difficulty, correct, timeMs, usedHint, mode: "practice"|"review"}`.
* **PII:** none beyond pseudonymous `userId`.

---

## 10) Visual design

* **Color:** calm blues/teals base, accent green for success, amber for warnings. High‑contrast theme flips backgrounds and removes gradients.
* **Typography:** Inter (default) + Atkinson Hyperlegible (toggle). Math in MathJax matching font size.
* **Density:** large tap targets (44×44px), generous spacing.
* **Icons:** simple line icons (e.g., lucide) with labels for clarity.

---

## 11) Item type specifics

### 11.1 Numeric entry

* On‑screen keypad with × ÷ ^ and fraction key; optional units dropdown.
* Accepts fractions, mixed numbers, decimals; shows canonicalized preview.

### 11.2 Multiple‑choice (single/multi)

* Large stacked options; select feedback with subtle hover; allow deselect.

### 11.3 Expression input

* Lightweight math input (no full CAS); allowed tokens shown as chips; live “simplified to …” helper.

### 11.4 Plot/graph

* 10×10 grid by default; pinch to zoom; keyboard arrows move point; screen‑reader announces coordinates.

### 11.5 Drag‑and‑drop

* Snapping slots with labels; keyboard alternative via list reordering control.

---

## 12) Review/printables

* Generate clean PDF packets (10/20/30 items) with QR to resume digitally; include answer key on second page optional.

---

## 13) Error handling & reporting

* **Report issue** captures itemId, screenshot of item card (client‑side render), last 10 console logs (sanitized), and user comment; queued offline if needed.

---

## 14) Performance budgets

* First load ≤ 2.5 s on 3G fast; JS ≤ 250 KB gzipped initial; lazy‑load MathJax and diagram components; cache templates.
* 60 fps for basic transitions; MathJax render hydrate within 100 ms on item switch.

---

## 15) Security & privacy (frontend)

* No storing access tokens in localStorage; use HTTP‑only cookies or session tokens in memory; rotate on resume.
* Obfuscate item answer in client; grading happens on server, but allow local pre‑checks for UX.
* COPPA/FERPA‑aligned UI (child‑appropriate copy, parent view via code).

---

## 16) QA checklist (UI)

* Keyboard‑only pass on all item types.
* Screen‑reader pass on sample items for each type.
* Offline scenario: practice 15 items, kill network, continue, restore network, verify sync and mastery reconcile.
* Mixed number acceptance tests; unit dropdown keyboard navigation.

---

## 17) Milestones for frontend build

* **M1:** Shell + Routing + Theme + Settings + Auth stub.
* **M2:** ItemPlayer (numeric + MC) + Hint + basic mastery bar + offline cache.
* **M3:** TEKS Map + Progress screens + Review builder + printables.
* **M4:** Plot/drag inputs + accessibility polish + analytics + error reporting.

---

## 18) Frontend data contracts (TypeScript types)

(High‑level; exact fields mirror backend contracts.)

```
export type LiveItem = {
  id: string; teks: string; type: 'numeric'|'mc'|'expression'|'plot'|'drag';
  seed: number; stimulus: any; prompt: string; options?: any[];
  answer_format: { form: 'int'|'fraction'|'decimal'|'mixed'|'label'; tolerance?: number; units?: string };
  hints: string[]; explanation?: string; difficulty: number;
};

export type Attempt = {
  id: string; itemId: string; userId: string; response: any; correct: boolean; timeMs: number; ts: number; usedHint?: boolean;
};

export type Mastery = { teks: string; score: number; attempts: number; lastSeenAt: number; dueReviewAt?: number };
```

---

## 19) Student data export (for parent/guardian)

* JSON file: profile, mastery per skill, attempt history (last 90 days), review schedule. Download from Settings.

---

## 20) Copy glossary (kid‑friendly)

* **Mastery:** “how strong you are at a skill”
* **Review:** “quick practice to keep skills fresh”
* **Hint:** “a little nudge to help”
* **Reteach:** “a mini‑lesson to refresh”

---

**End of UI/UX Spec**
