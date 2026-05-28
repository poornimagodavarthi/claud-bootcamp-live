---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Closing Block'
paginate: true
size: 16:9
title: "Part 11 — Q&A, Exam Briefing & Next Steps"
description: "Closing block: common mistakes, prompting anti-patterns, certification rules, and what to do Monday morning."
---

<!-- duration: 30 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Closing block · 30 min</span>

# Q&A, Exam Briefing & Next Steps

Claude Code Bootcamp · Day 1 · Closing the loop

<img class="hero-icon" src="themes/icons/award.svg" alt="" />

---

<!-- _class: tpl-objectives -->

## Promise

In 30 minutes you will:

1. Spot the **5 most common mistakes** AI-paired developers make
2. Avoid the **prompting anti-patterns** that wreck loops
3. Understand the **certification rules** (40/40/20, 70% pass)
4. Walk out with a **Monday morning plan** to keep momentum

---

## Why this matters

The hour you spend right now is the difference between "interesting workshop" and "habit that ships software".

- Today you wrote code with Claude.
- Tomorrow you have to do it **alone, on a deadline, on your own repo**.
- The closing block locks the loop: mistakes, fixes, certification, what to do next.

If you skip this block you'll leave with technique and no system.

---

<!-- _class: tpl-show -->

## Concepts

Three frameworks that travel with you:

| Framework | Use when | Source |
|---|---|---|
| **Plan → implement → test → review → commit loop** | Every non-trivial change | Module 1 |
| **40/40/20 evaluation rubric** | Grading any AI output | Module 5 + Assessment |
| **12-item production-readiness checklist** | Before tagging a release | Module 10 + `skills/release-readiness` |

> Each framework is a **checklist**, not a vibe. Print them.

---

<!-- _class: tpl-show -->

## Live demo flow

3 anti-patterns, demonstrated and fixed in 8 minutes:

1. **The "fix it" loop** — vague prompt → unfocused diff → re-prompt → drift.
   Fix: paste the exact error + the smallest reproducer.
2. **The over-eager agent** — long autonomous run → wrong abstraction → 600-line diff.
   Fix: stop at the plan, review, **then** implement.
3. **The merged-without-review commit** — Claude writes commit + push in one shot.
   Fix: review-before-commit, even when it's "obviously fine".

Each fix is a **shorter prompt**, not a longer one.

---

<!-- _class: tpl-try -->

## Mini project

Open the repo you came in with (your own project, not the bootcamp).

1. Pick **one** change you've been putting off (a refactor, a test, a doc).
2. Apply the 5-step loop with Claude Code, **on the clock — 15 minutes**.
3. Stop at the commit. Do not push.

> Success: you have a reviewable diff and a one-paragraph summary of what changed.

---

<!-- _class: tpl-try -->

## Step-by-step lab

If you don't have your own repo ready, use today's deliverables:

1. Open `exercises/part-10/` and run `skills/release-readiness/SKILL.md` against any module deliverable from today.
2. Produce the 12-item table.
3. Decide GO / NO-GO with a one-sentence justification.

Time-box: 12 minutes.

---

## Suggested Claude Code prompts

```text
# 1. Loop reset when Claude drifts
"Stop. Show me the next single step you intend to take and why. Do not write code yet."

# 2. Self-review before commit
"You are reviewing a stranger's PR. List every potential bug, ranked by severity. Smallest patch each."

# 3. Honest readiness verdict
"Walk my last commit through the 12-item production-readiness checklist. End with GO or NO-GO and a list of blocking item numbers."
```

---

## Deliverable checklist

- [ ] One mini-deliverable (today's lab OR your own repo) reviewed
- [ ] GO / NO-GO verdict written down
- [ ] Knowledge quiz attempted (`assessments/knowledge-quiz.md`)
- [ ] Practical task chosen (`assessments/practical-task.md`)
- [ ] Code-review reflection drafted (`assessments/code-review-reflection.md`)

---

## Definition of done

You are "done" with the bootcamp when:

1. The three assessment artefacts are in your submission zip.
2. Your weighted score against `assessments/rubric.md` is **≥ 70%**.
3. You can name, from memory, the **5 May 2026 pillars**: Skills · Hooks · MCP · GitHub Actions · Multi-agent.
4. You have a one-sentence answer to *"What will I try in my own repo on Monday?"*

---

## Review checkpoint

Go around the room (or chat) and complete this sentence:

> "On Monday, I will use Claude Code to ___ on my project ___ , and I will stop the loop when ___ ."

If you can't finish the sentence, re-watch the Part 9 recording before submitting.

---

## Common mistakes

The five we see every cohort:

1. **No plan slide** — jumping straight into "write the function".
2. **Skipping the review pass** — accepting the first diff.
3. **Letting Claude commit** — losing the human checkpoint.
4. **Treating skills as files** — instead of habits invoked deliberately.
5. **No CLAUDE.md** — Claude has no project context, you re-pay onboarding cost every session.

Each maps to a module: 1, 5, 6, 9, 3.

---

## Instructor notes

Cut-line if running short:

- **Cut first**: the "Step-by-step lab" slide (let students do it offline).
- **Keep**: Common mistakes, Definition of done, the Monday-morning sentence.
- **Never cut**: the assessment briefing — students need to know how grading works.

Cohort notes (2026-05-30 inaugural):
- Watch for a flat-energy room at this point; insert a 2-minute stretch.
- Hand out the certification template URL only after Q&A.

---

## Transition

Three things, in this order, before you close your laptop:

1. **Upload** your zip to the Packt LMS.
2. **Star** the repo so you can find the skills library on Monday.
3. **Write** your Monday-morning sentence somewhere you'll see it (Slack DM to yourself works).

You have everything you need. Now ship.

<!-- polish-log
2026-05-28 · feature 005 · initial draft of closing block (R-002).
-->
