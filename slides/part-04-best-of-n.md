---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 04'
paginate: true
size: 16:9
title: "Module 4 — Build Faster with Best-of-N"
description: "Generate N candidates for the same task and select the winner using a 3-criterion rubric. Ship a Notes API."
---

<!-- duration: 30 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 04 · 30 min</span>

# Build Faster with Best-of-N

**The first answer is rarely the best. Generate three; score; ship the winner.**

<img class="hero-icon" src="themes/icons/play.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "We exploit variance on purpose — three independent shots, one rubric, one winner."
-->

---

<!-- _class: tpl-objectives -->

## Theory · Best-of-N (4 min)

> **Generate N independent candidates → score on a rubric → pick the winner.** N = 3 is the sweet spot.

- **Independent** — each candidate gets its own fresh prompt context. *Not* "now improve it" (that's iteration).
- **Score on a rubric**, not vibes. Three criteria:
  - **Correctness** — passes the manual test plan?
  - **Simplicity** — could a junior maintain it?
  - **Fit** — matches `CLAUDE.md` conventions and repo style?

**Without the rubric you pick by gut and the lift disappears. Correctness gates everything.**

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- Stress: BoN != iteration. Iteration converges on one lineage; BoN samples the space.
-->

---

<!-- _class: tpl-show -->

## Best-of-N, scored

![Best-of-N: generate N candidates, score on Correctness, Simplicity, Fit, pick the winner](intermediate/assets/04-bon-scoring.svg)

Generate **N** independent candidates → score on **Correctness · Simplicity · Fit** → keep the winner.

<!--
SPEAKER NOTES — slide 3 (diagram, 1 min)
- The scorecard on the next slide is the right-hand column of this picture.
-->

---

<!-- _class: tpl-show -->

## Reference · The 3-criterion scorecard

| Criterion | Question | Weight |
|---|---|---|
| **Correctness** | Does it pass every step of the manual test plan? | Gate — fail here = out |
| **Simplicity** | Could a junior maintain it next quarter? | High |
| **Fit** | Does it follow `CLAUDE.md` + repo style? | Medium |

Record a one-paragraph justification per candidate in `scoring.md`. **Never delete losers before scoring.**

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- One candidate + "improve it" ×3 (iteration, not BoN).
- Skipping the rubric → picking by vibe → no lift.
- Choosing the "elegant" one that fails the test plan (correctness is the gate).

<!--
SPEAKER NOTES — slide 4 (common mistakes, 30 sec)
Instructor cues:
- Score side-by-side; show the losers so the lift is visible.
-->

---

<!-- _class: tpl-show -->

## Live demo · Three candidates, one winner (6 min)

**The reusable prompt — paste it verbatim for A, B, and C:**

```text
GOAL: A REST Notes API: create, list, get, delete a note.
CONSTRAINTS: Python 3.11 + FastAPI; persist to SQLite ./notes.db;
  return JSON; 404 on missing id; no other third-party deps.
OUTPUT: one runnable app + a curl test plan covering all 4 routes.
EXAMPLES: POST /notes {"text":"hi"} -> 201 + id;
  GET /notes/999 (missing) -> 404 {"error":"not found"}.
```

`/clear` before **each** candidate → paste the **same** prompt → save to `candidate-a|b|c/`. Then score side-by-side and commit the winner.

> Variance must come from the model, **not** the prompt. Never say "now do it differently."

<!--
SPEAKER NOTES — slide 5 (demo, 6 min)
- The mechanism is independence: `/clear` between each candidate so no shared history leaks.
- Paste the EXACT same prompt all three times — variance must come from the model, not the prompt.
- A new terminal tab / new chat session works too; the point is zero carried-over context.
- Tip: `claude -p "$(cat prompt.txt)"` three times is the scriptable version.
- Success signal: the winner passes the curl test plan; at least one loser visibly doesn't.
-->

---

<!-- _class: tpl-try -->

## Your turn · Notes API, Best-of-3 (13 min)

**Exercise**: [`exercises/part-04/README.md`](../exercises/part-04/README.md)

Build a Notes API (SQLite `notes.db`), then generate **3 candidates** and score them:

```text
POST /notes · GET /notes?q= · GET /notes/:id · PATCH /notes/:id · DELETE /notes/:id
Status: 201 create · 200 read/update · 204 delete · 404 missing · 422 invalid
```

Track A: Python (FastAPI + Pydantic v2). Track B: Node (Hono + Zod + better-sqlite3).

**Deliverables**: `candidate-{a,b,c}/`, `scoring.md` (scores + justification), `winner/` (clean copy).

**Success signal**: all five endpoints respond with correct status codes via curl.

<!--
SPEAKER NOTES — slide 6 (hands-on, 13 min)
- Hold them to three independent prompts. Walk the room and check candidate folders exist.
- 3-min warning. Stuck students: score what they have; partial BoN still teaches the loop.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] Three candidates in `module-04/candidate-{a,b,c}/`.
- [ ] `scoring.md` with scores + one-paragraph justification each.
- [ ] `winner/` runs end-to-end; losers archived (not deleted).

**Next** — we trust the winner only after we *test* it and review like a stranger's PR.
**Module 5 — Testing, Debugging & Self-Review.**

<!--
SPEAKER NOTES — slide 7 (wrap, 1 min)
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (matches Module 1 pilot).
cover -> theory (BoN) -> reference (scorecard · mistakes) -> live demo -> your turn -> done.
-->
