---
marp: true
theme: default
paginate: true
size: 16:9
title: "Module 1 — Welcome, Setup & AI-First Mindset"
description: "Set the room up for 4 hours of high-velocity AI-paired delivery. Introduce the Plan→Implement→Test→Review→Commit loop."
---

<!-- duration: 20 min -->

## Module 1 — Welcome, Setup & AI-First Mindset

Claude Code Bootcamp · Day 1 · Block 1 of 10
Instructor: **Luca Berton** · Endorsed by **Packt Certification**

---

## Promise

By the end of this 20-minute block you will:

1. Have verified your pre-work environment (Claude Code, Python 3.11+, Node.js 20+, Git).
2. Know exactly how the next 4 hours of instruction are structured.
3. Be able to name the five steps of the **AI coding loop** we will reuse in every module.

---

## Why this matters

- We are building **10 small projects in 4 hours**. That is impossible by hand. It is achievable when you treat Claude Code as a junior engineer that you direct, review, and merge.
- The cost of "spray-and-pray" prompting compounds: bad prompt → bad code → bad tests → wasted module. A repeatable loop keeps you above the line.
- Production teams using AI-paired coding report 30–50% throughput gains *only when* they use a loop. Everyone else regresses on quality.

---

## Concepts

- **AI-paired coding**: you stay the engineer of record. Claude proposes; you decide.
- **The loop**: **Plan → Implement → Test → Review → Commit.** Every module repeats this.
- **The skill library**: reusable instructions to Claude that survive across projects (`skills/`).
- **Definition of Done**: a hard checklist per module; if it isn't checked, the module isn't shipped.
- **Submission as proof of work**: every module produces a folder in your final zip.

---

## Live demo flow

1. Instructor opens this repo in their IDE with Claude Code attached.
2. Runs `git status` — clean. Runs `python3 --version` and `node --version` — both green.
3. Asks Claude: *"List the top-level files and tell me what kind of repository this is."*
4. Class watches Claude read the repo and respond with the answer everyone produced in pre-work.
5. Instructor narrates the 5-step loop while Claude is responding.

---

## Mini project

**Verify your AI Coding Workspace.**

Deliverable for module 1 in your submission zip: `module-01/` containing

- `environment.txt` — output of `python3 --version`, `node --version`, `git --version`
- `loop-notes.md` — your one-paragraph explanation of the 5-step loop, written in your own words

---

## Step-by-step lab

1. Open a terminal. Run the three `--version` commands; pipe to `module-01/environment.txt`.
2. In Claude Code, paste the prompt below.
3. Read Claude's reply. Edit it into your own one-paragraph explanation.
4. Save it to `module-01/loop-notes.md`.
5. Tick the Definition of Done.

---

## Suggested Claude Code prompts

```text
You are onboarding a new engineer who has never used AI-paired coding.
In one short paragraph (max 6 sentences), explain the loop:
Plan → Implement → Test → Review → Commit.
Use the metaphor of directing a junior engineer.
End with one sentence about why skipping the Review step is the most common failure mode.
```

---

## Deliverable checklist

- [ ] `module-01/environment.txt` contains three valid version strings.
- [ ] `module-01/loop-notes.md` exists and is non-empty.
- [ ] The notes name all five steps of the loop in order.
- [ ] The notes are in **your own words**, not Claude's verbatim output.

---

## Definition of done

✅ Environment verified · ✅ Loop explained in your own words · ✅ Submission folder `module-01/` exists with both files.

---

## Review checkpoint

Pair with the person next to you. In 60 seconds each:

- Read each other's `loop-notes.md`.
- Identify one sentence you would tighten.
- Confirm both `environment.txt` files show identical major versions.

---

## Common mistakes

- Copying Claude's reply verbatim — instructor scoring penalises this.
- Treating "Review" as optional. Skipping review is how AI-generated bugs reach production.
- Using PowerShell on Windows. Move to WSL2 (see `student-guide.md`).
- Pre-work skipped — you cannot keep up; pair with a neighbor for module 1 only.

---

## Instructor notes

- Keep this block to 20 min hard. Mindset only — **no live installs**.
- Open with Claude Code on a known repo, not a slide.
- If a student's environment is broken, mark them as paired and continue.
- Reference the schedule table in `README.md`. Set expectations on break placement.

---

## Transition to next module

Now that the loop is named, we apply step 1 — **Plan** — by writing prompts the way a Tech Lead writes specs.
**Next: Module 2 — Prompting Like a Tech Lead.**
