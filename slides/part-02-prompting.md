---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 02'
paginate: true
size: 16:9
title: "Module 2 — Prompting Like a Tech Lead"
description: "Translate a vague feature request into a precise, constraint-rich prompt. Ship a CLI Task Manager in one pass."
---

<!-- duration: 24 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 02 · 24 min</span>

# Prompting Like a Tech Lead

**A great prompt is a spec. Write it the way a Tech Lead writes a ticket.**

<img class="hero-icon" src="themes/icons/pencil.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "Today we turn a vague idea into a one-pass CLI."
- Tease the demo: same task, vague prompt vs GCOE prompt, watch the lift.
-->

---

<!-- _class: tpl-objectives -->

## Theory · The GCOE prompt (4 min)

A production prompt has **four parts — skip one and quality drops**:

> **G**oal · **C**onstraints · **O**utput format · **E**xamples

- **Goal** — one verb-led sentence: what can the user *do* at the end?
- **Constraints** — language, deps, file layout, error handling, and what must **not** happen.
- **Output format** — files, exit codes, JSON shapes if any.
- **Examples** — one happy path + one edge case is enough to disambiguate.

**A vague prompt produces plausible code that fails review. GCOE produces code you can merge.**

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- Anchor: constraints are where the engineering lives. "No third-party deps" is a design decision.
- Examples aren't optional — the model uses them to resolve ambiguity.
-->

---

<!-- _class: tpl-show -->

## Anatomy of a GCOE prompt

![GCOE prompt anatomy: Goal, Constraints, Output, Examples](intermediate/assets/02-prompt-anatomy.svg)

**G**oal · **C**onstraints · **O**utput · **E**xamples — skip one and quality drops.

<!--
SPEAKER NOTES — slide 3 (diagram, 1 min)
- Point at each block; the skeleton on the next slide maps 1:1 to this picture.
-->

---

<!-- _class: tpl-show -->

## Reference · GCOE skeleton you can paste

```text
GOAL: A user can <verb> <thing> from the command line.

CONSTRAINTS:
- Language: Python 3.11, standard library only (no third-party deps).
- Persist state to ./tasks.json.
- Exit codes: 0 success, 1 user error, 2 internal error.

OUTPUT:
- A single runnable script + a short README with usage.

EXAMPLES:
- `task add "Buy milk"` -> prints new id, exit 0.
- `task done 999` (missing id) -> prints error to stderr, exit 1.
```

Keep it tight. Every line removes one wrong guess Claude could make.

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
- This is the students' copy-paste starting point for the exercise.
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- "Build a CLI" with no constraints — looks fine, fails review.
- Allowing unintended third-party deps (the constraint exists for a reason).
- Skipping examples and exit codes — production CLIs are graded on exit codes, not stdout.

<!--
SPEAKER NOTES — slide 4 (common mistakes, 30 sec)
Instructor cues:
- Show the vague-vs-GCOE diff live; let the lift sell itself.
- Delete one constraint mid-demo to show the regression.
-->

---

<!-- _class: tpl-show -->

## Live demo · Vague vs. GCOE (5 min)

**Step 1 — paste the vague prompt:**

```text
Make a CLI to manage tasks.
```

**Step 2 — paste the GCOE prompt and re-run:**

```text
GOAL: A user can add, list, complete, and delete tasks from the command line.
CONSTRAINTS: Python 3.11, stdlib only; persist to ./tasks.json;
  exit codes 0 success / 1 user error / 2 internal error.
OUTPUT: one runnable script + a short usage README.
EXAMPLES: `task add "Buy milk"` -> prints id, exit 0;
  `task done 999` -> stderr error, exit 1.
```

**Success signal**: the GCOE version runs all four commands with correct exit codes; the vague one doesn't.

<!--
SPEAKER NOTES — slide 5 (demo, 5 min)
- Run vague first, show generic output (no persistence, no exit codes).
- Run GCOE, show the lift: real CLI, tasks.json, tests scaffolded.
- Then DELETE the "stdlib only" constraint and re-run -> show the regression.
- Keep the two outputs side by side. The contrast is the lesson.
-->

---

<!-- _class: tpl-try -->

## Your turn · CLI Task Manager (12 min)

**Exercise**: [`exercises/part-02/README.md`](../exercises/part-02/README.md)

Build a CLI with four commands, persisted to `tasks.json`:

```text
task add "<title>"        # -> prints new id
task list [--status STATE]
task done <id>
task delete <id>
```

**Prompt**: start from the GCOE skeleton; fill Goal/Constraints/Output/Examples for *your* task manager.

**Deliverable**: working CLI in `module-02/` + `iteration-notes.md` recording one deleted constraint and its code diff.

**Success signal**: all four commands run end-to-end; exit codes are `0` / `1` / `2`.

<!--
SPEAKER NOTES — slide 6 (hands-on, 12 min)
- Walk the room. Catch students who skipped Constraints — that's where they lose points.
- 3-min warning. Anyone stuck: have them paste their prompt and grade it against GCOE out loud.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] Four commands work; `tasks.json` round-trips state.
- [ ] Exit codes correct (`0` / `1` / `2`).
- [ ] `iteration-notes.md` documents one deleted constraint + diff.

**Next** — a good prompt is per-task. Now we make Claude follow your repo's rules *automatically*.
**Module 3 — Project Context with CLAUDE.md.**

<!--
SPEAKER NOTES — slide 7 (wrap, 1 min)
- Bridge: "GCOE every time is tiring. Module 3 bakes the constraints into the repo."
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (matches Module 1 pilot).
cover -> theory (GCOE) -> reference (skeleton · mistakes) -> live demo -> your turn -> done.
-->
