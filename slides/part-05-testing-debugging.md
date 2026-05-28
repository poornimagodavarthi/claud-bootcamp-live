---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 05'
paginate: true
size: 16:9
title: "Module 5 — Testing, Debugging & Self-Review"
description: "Write a real test suite for the module 4 API, plant and fix two bugs, and ship your personal Code Review Rubric."
---

<!-- duration: 28 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 05 · 28 min</span>

# Testing, Debugging & Self-Review

**Untested AI code is a guess. Make Claude review its own work as a stranger's PR.**

<img class="hero-icon" src="themes/icons/shield.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "We test the Module 4 winner, plant bugs, and let Claude catch them — with the right framing."
-->

---

<!-- _class: tpl-objectives -->

## Theory · Test, then self-review (4 min)

**Test pyramid for AI code**: many cheap unit tests · a few integration tests on the happy path · always cover **error paths**.

> **Self-review prompt**: ask Claude to find bugs *as if reviewing a stranger's PR.* The framing kills sycophancy.

- Off-by-one and **boundary** bugs are Claude's blind spot — always test boundaries.
- Bundled skills cut prompt repetition: `/debug` · `/verify` · `/code-review` · `/loop` · `/batch`.
- You ship a **personal** `code-review-rubric.md` — your blind spots, not the instructor's.

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- The "stranger's PR" phrase is the whole trick — say it twice.
-->

---

<!-- _class: tpl-show -->

## The test-and-review loop

![Test and debug loop: write tests, find the bug, self-review, fix, re-run](intermediate/assets/05-test-debug-loop.svg)

Tests → find the bug → **self-review as a stranger** → fix → re-run until green.

<!--
SPEAKER NOTES — slide 3 (diagram, 1 min)
- The self-review step is the one humans skip; that's where the rubric lives.
-->

---

<!-- _class: tpl-show -->

## Reference · The self-review prompt

```text
Review this code as if it were a stranger's pull request.
List every bug, edge case, and boundary error you can find.
Be specific: file, line, symptom, and the fix. Do not be polite.
```

Test in-process with a temp SQLite DB per test — **no network, no HTTP mocks, never mock the system under test.**

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- Tests that mock the system under test (useless).
- Self-review without the "stranger's PR" framing (sycophantic output).
- Copying the skill rubric verbatim — your rubric must reflect *your* blind spots.
- Confusing the student rubric with the instructor grading rubric (different files).

<!--
SPEAKER NOTES — slide 4 (common mistakes, 30 sec)
Instructor cues:
- Plant the first bug live; let the class plant the second.
-->

---

<!-- _class: tpl-show -->

## Live demo · Plant a bug, catch it (6 min)

1. Open the Module 4 winner; ask for a test suite (pytest + httpx, or vitest + fetch). Run → green.
2. Plant one off-by-one bug live (e.g. a pagination boundary).
3. Paste the **self-review prompt** verbatim:

```text
Review this code as if it were a stranger's PR you must approve.
List concrete bugs with file, line, and a minimal fix. Don't say "looks good".
```

4. Claude finds it → fix → re-run. Repeat with a second seeded bug.

**Success signal**: the self-review names the bug's file, line, and fix — not "looks good".

<!--
SPEAKER NOTES — slide 5 (demo, 6 min)
- If Claude misses the bug, that's a teachable moment: refine the framing, don't accept the miss.
-->

---

<!-- _class: tpl-try -->

## Your turn · Suite + 2 bugs + your rubric (11 min)

**Exercise**: [`exercises/part-05/README.md`](../exercises/part-05/README.md)

1. Write a full suite: create, list, search, get-one, update, delete, 404, 422.
2. Plant **two** seeded bugs (from the reference), use the self-review prompt to fix them.
3. Author `code-review-rubric.md` — ≤ 1 page, 5–8 checks, focused on Claude's blind spots.

**Deliverables**: green suite · `bug-fix-notes.md` (symptom → cause → diagnosis → fix) · personal rubric.

**Success signal**: tests pass on fixed code; rubric has ≥ 1 check not in `skills/code-review/SKILL.md`.

<!--
SPEAKER NOTES — slide 6 (hands-on, 11 min)
- Walk the room. Catch students mocking the app itself. 3-min warning before wrap.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] Test suite runs green on fixed code.
- [ ] `bug-fix-notes.md` documents both bugs (symptom, cause, diagnosis, fix).
- [ ] Personal rubric with ≥ 1 original check.

**Next** — tested code earns a safe path to main: branches, atomic commits, a real PR.
**Module 6 — Git Workflows for Safe AI Dev.**

<!--
SPEAKER NOTES — slide 7 (wrap, 1 min)
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (matches Module 1 pilot).
cover -> theory (test + self-review) -> reference (prompt · mistakes) -> live demo -> your turn -> done.
-->
