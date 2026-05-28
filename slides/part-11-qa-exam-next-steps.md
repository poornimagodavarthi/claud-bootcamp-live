---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Part 11'
paginate: true
size: 16:9
title: "Part 11 — Q&A, Exam Briefing & Next Steps"
description: "Closing block: common mistakes, prompting anti-patterns, certification rules, and what to do Monday morning."
---

<!-- duration: 30 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Part 11 · 30 min · Closing</span>

# Q&A, Exam Briefing & Next Steps

**Ten projects done. Now: the three frameworks you keep, the exam, and Monday.**

<img class="hero-icon" src="themes/icons/award.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "This block is the bridge from workshop to your real repo."
-->

---

<!-- _class: tpl-objectives -->

## Theory · Three frameworks you keep (4 min)

Forget the syntax; keep these three:

1. **The loop** — Plan → Implement → Test → Review → Commit (every non-trivial change). *Module 1.*
2. **The 40/40/20 rubric** — grade any AI output: 40% correctness · 40% quality · 20% fit. *Module 5 + assessment.*
3. **The readiness checklist** — five axes before you tag a release. *Module 10.*

> If you remember nothing else, remember the loop. It is the whole course in five words.

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- These three transfer to any model, any tool, any repo. That's the carry-out.
-->

---

<!-- _class: tpl-show -->

## Reference · The five most common mistakes

1. **No plan** — jumping straight to "write the function".
2. **Skipping review** — accepting the first diff.
3. **Letting Claude commit** — losing the human checkpoint.
4. **Treating skills as files** instead of habits invoked deliberately.
5. **No CLAUDE.md** — re-explaining stack + conventions every session.

Every one is a habit, not a knowledge gap. Fix the habit.

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
- Ask the room which one they're most guilty of. Quick show of hands.
-->

---

<!-- _class: tpl-show -->

## Reference · Three prompting anti-patterns

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **"Fix it" loop** | Vague prompt → unfocused diff → re-prompt → drift | Paste the exact error + smallest reproducer |
| **Over-eager agent** | Long run → wrong abstraction → 600-line diff | Stop at the plan, review, *then* implement |
| **Merge-without-review** | Claude commits + pushes in one shot | Review-before-commit, even when "obviously fine" |

<!--
SPEAKER NOTES — slide 4 (reference, 3 min)
- Demo each anti-pattern + its fix if time allows. Otherwise narrate from the table.
-->

---

<!-- _class: tpl-show -->

## Live demo · "Fix it" loop vs. precise prompt (4 min)

1. Reproduce the **"fix it" loop** — vague prompt → unfocused diff → drift:

```text
It's broken, fix it.
```

2. Reset. Paste the precise prompt — exact error + smallest reproducer:

```text
GET /notes/999 returns 500, expected 404. KeyError 'note' in get_note() line 42.
Fix only this; keep all other behavior. Show the diff.
```

3. Narrate: the difference between coaching and guessing.

**Success signal**: the precise prompt fixes it in one pass; the vague loop doesn't.

<!--
SPEAKER NOTES — slide 5 (demo, 4 min)
-->

---

<!-- _class: tpl-show -->

## Exam briefing · How to pass

**Submit (zip to the Packt LMS):**

- The three assessment artefacts from `assessments/`: knowledge-quiz · practical-task · code-review-reflection.
- Weighted score **≥ 70%** against [`assessments/rubric.md`](../assessments/rubric.md).

**Be ready to:**

- Name the five May 2026 pillars from memory: **Skills · Hooks · MCP · GitHub Actions · Multi-agent**.
- Answer in one sentence: *"What will I try in my own repo on Monday?"*

<!--
SPEAKER NOTES — slide 6 (exam, 3 min)
- Read the 70% bar out loud. Point students at the rubric file now.
-->

---

<!-- _class: tpl-show -->

## Future-proof · Keep an eye on (May 2026 → beyond)

The tools change monthly; the **habits** don't. What to watch — and the trick that compounds:

| Watch in 2026 | Trick that makes life better |
|---|---|
| **Shared skill libraries** across teams | Keep a `skills/` folder in every repo — borrow habits, don't reinvent |
| **MCP servers** for more of your stack | Wire issue tracker · CI · observability in once; verify with `/mcp` |
| **Multi-agent** orchestration maturing | Delegate parallel work, keep **one** human reviewer — you |
| **Hooks** as default guardrails | Auto-format, secret-scan, test-gate on every action |
| Bigger context + **memory files** | Pin model + conventions in `CLAUDE.md`; it still wins |

> The rule that survives every release: **Plan → Implement → Test → Review → Commit.**

<!--
SPEAKER NOTES — slide 7 (future-proof, 2 min)
- Theme: chase habits, not features. Every 2026 capability amplifies the loop, never replaces the reviewer.
- Tell them to bookmark the repo's skills/ folder as their starting point Monday.
-->

---

<!-- _class: tpl-try -->

## Your turn · The Monday sentence (3 min)

No code this time — one sentence. Complete it and write it where you'll see it:

> *"On Monday, I will use Claude Code to **\_\_\_** on my project **\_\_\_**, and I will stop the loop when **\_\_\_**."*

Then:

- Upload your submission zip to the Packt LMS.
- ⭐ Star the repo so you can find the skills on Monday.

**Success signal**: you can say your Monday sentence out loud without hesitating.

<!--
SPEAKER NOTES — slide 8 (3 min)
- If a student can't complete the sentence, send them to re-watch Module 9 before submitting.
-->

---

<!-- _class: tpl-done -->

## Done · You're certified-ready (1 min)

**Definition of done — the whole bootcamp**

- [ ] Three assessment artefacts in the submission zip.
- [ ] Weighted score ≥ 70% against the rubric.
- [ ] Can name the five May 2026 pillars from memory.
- [ ] Have your one-sentence Monday answer.

**Thank you.** You direct, you review, you merge — you're the engineer of record. Go ship.

<!--
SPEAKER NOTES — slide 9 (close, 1 min)
- End on the through-line: the loop goes home with them. Open the floor for Q&A.
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (closing variant: no hands-on exercise).
cover -> theory (3 frameworks) -> reference (mistakes · anti-patterns) -> live demo -> exam briefing
      -> your turn (Monday sentence) -> done.
-->
