# Quickstart: Teach Module 1 in Under 30 Minutes

**Audience**: a new instructor (not the author) who just cloned this repository.
**Goal**: From `git clone` to "module 1 is on screen and ready to teach" in **≤ 30 minutes** (spec SC-001).
**Date**: 2026-05-21

This document doubles as the **release smoke test**: if any step fails
on a fresh machine, the release is not ready.

---

## Prerequisites

You need:

- A computer running macOS, Linux, or Windows-with-WSL2 (FR-027a).
- Node.js 20+ installed (`node --version`).
- Git 2.40+ installed (`git --version`).
- An authenticated Claude Code session (`claude --version` and a sample
  query work).
- ~5 minutes of network bandwidth for first-time Marp/Chromium downloads.

You do **not** need Python, Docker, or any cloud account to teach
module 1. Python is required only when teaching modules 2, 4, 5, 7, 8.

---

## 30-minute path

### 1. Clone (≤ 1 min)

```bash
git clone <repo-url> claude-code-bootcamp
cd claude-code-bootcamp
```

### 2. Build the slide decks (≤ 5 min, mostly first-run downloads)

```bash
cd slides
./deploy-pptx.sh
```

Expected:

- Output `dist/pptx/part-01-setup-mindset.pptx` (and 9 other module decks) appears.
- Exit code `0`.
- First run downloads Marp + Chromium via `npx`; subsequent runs are seconds.

If Chromium cannot download, set `CHROME_PATH` to your existing Chrome/Edge/Brave executable and rerun.

### 3. Open the instructor guide (≤ 2 min)

```bash
$EDITOR ../instructor-guide.md
```

Read these sections:

- "Pre-flight checklist"
- "Module 1 facilitation notes"
- "If running short" (per-module cuts)
- "Grading & certificate issuance"

### 4. Open module 1 deck (≤ 2 min)

```bash
open dist/pptx/part-01-setup-mindset.pptx        # macOS
xdg-open dist/pptx/part-01-setup-mindset.pptx    # Linux
```

Or preview live in your browser:

```bash
npx --yes @marp-team/marp-cli@latest --server .
# open http://localhost:8080/part-01-setup-mindset.md
```

Verify visually that the deck contains all 14 required sections in
order: Title → Promise → Why this matters → Concepts → Live demo flow →
Mini project → Step-by-step lab → Suggested Claude Code prompts →
Deliverable checklist → Definition of done → Review checkpoint →
Common mistakes → Instructor notes → Transition to next module.

### 5. Run the validator (≤ 1 min)

From the repo root:

```bash
./scripts/validate.sh
```

Expected: prints `OK` for each of the structural checks (10 decks,
10 exercises, 10 skills, dual-license files, schedule sums to 240 ± 5,
gitignore covers `slides/dist/`, no naming collisions).

A clean exit code of `0` means the repository is in a **release-ready**
state.

### 6. Verify pre-work guidance (≤ 3 min)

Open `student-guide.md` and locate the **Pre-work** section. Confirm:

- Pre-work is described as **mandatory** and ≤ 30 min self-paced.
- The 4-step smoke test is documented (Python/Node version checks, Git
  version, Claude Code auth, "hello-Claude" prompt against this repo).
- Output capture is required (students bring their smoke-test output
  to the live session).

This matches FR-025a and lets you trust that students arrive ready.

### 7. Confirm submission & grading workflow (≤ 3 min)

Open `instructor-guide.md` and locate the **Grading** section. Confirm:

- Students upload a single zip to the Packt LMS / shared drive (FR-023a).
- The zip layout is documented (one folder per module + assessments).
- The instructor grades locally against `assessments/rubric.md` and
  records the score in the LMS.
- `assessments/answer-key.md` provides the quiz answers.
- `certificate-template.md` is issuable on ≥ 70% pass.

### 8. Sanity-check one reference solution (≤ 5 min)

Pick module 2 and run its Python reference solution as a smoke test:

```bash
cd exercises/part-02/solution/python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m tasks add "Buy milk"
python -m tasks list
```

Expected: the CLI works end-to-end. (Repeat for the Node track if you
plan to teach that variant.)

### 9. You are ready to teach (≤ 8 min remaining)

You should have ~5–10 minutes of buffer. Use it to:

- Review your "Common mistakes" callouts for module 1.
- Confirm your screen-share zoom level on the deck (16:9 should fill
  the window).
- Have `instructor-guide.md` open in a second window for live reference.

---

## Total budget

| Step | Budget | Notes |
|---|---|---|
| Clone | 1 min | |
| Build decks | 5 min | First run only; cached after |
| Read instructor guide | 2 min | |
| Open module 1 | 2 min | |
| Run validator | 1 min | |
| Verify pre-work guidance | 3 min | |
| Confirm grading workflow | 3 min | |
| Smoke-test a reference solution | 5 min | Optional but recommended |
| Buffer | 8 min | |
| **Total** | **30 min** | |

---

## What "ready" looks like

- Slide build exits 0; PPTX files for all 10 modules under `slides/dist/pptx/`.
- `scripts/validate.sh` exits 0.
- Module 1 deck opens and contains all 14 sections.
- Instructor guide and student guide cover pre-work, live delivery, grading, and certificate issuance.
- At least one reference solution runs successfully on your machine.

If any of those fail, the repository is **not** release-ready.
File an issue or block the release until fixed.
