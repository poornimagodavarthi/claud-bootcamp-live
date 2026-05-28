---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 10'
paginate: true
size: 16:9
title: "Module 10 — Production Readiness"
description: "Pick one project from today and write a Production Readiness Report across 5 axes. Decide go / no-go."
---

<!-- duration: 18 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 10 · 18 min</span>

# Production Readiness

**"It runs on my laptop" is not "ready to ship." Make the call across five axes.**

<img class="hero-icon" src="themes/icons/award.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "We pick one project from today and decide, honestly, go or no-go."
-->

---

<!-- _class: tpl-objectives -->

## Theory · Five axes + a verdict (4 min)

Score every shipping candidate on five axes that **always** matter:

> **Security · Observability · Deployment · Runbooks · Rollback**

- For each axis: one **status** (🟢/🟡/🔴) · one **biggest risk** · one **smallest next step**.
- Use [`skills/production-readiness-review/SKILL.md`](../skills/production-readiness-review/SKILL.md) as the durable instrument.
- **Go / no-go is a decision, not a vibe.** End with a verdict and a ≤ 25-word rationale.

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- Push honesty: after one workshop, "all green" is almost never true.
-->

---

<!-- _class: tpl-show -->

## The five readiness axes

![Five production-readiness axes: Security, Observability, Deployment, Runbooks, Rollback](intermediate/assets/10-five-axes.svg)

**Security · Observability · Deployment · Runbooks · Rollback** → one go/no-go verdict.

<!--
SPEAKER NOTES — slide 3 (diagram, 1 min)
- Each spoke gets a status; the hub is the verdict.
-->

---

<!-- _class: tpl-show -->

## Reference · Overeager agents (May 2026)

arXiv **2605.18583**: agents routinely take **out-of-scope** actions on benign tasks — editing unrequested files, running unapproved commands, silently expanding scope.

**Defences, in order:**

- **Least-privilege tools** — grant only what this task needs.
- **Permission modes** — `ask` for shell · `deny` for network · `read-only` zones.
- **Shell approval** — every command requires a tap until trust is earned.
- **Review before commit** — diff-first, always; never `--no-verify`.
- **Disaster recovery** — clean branch, atomic commits, easy `git reset --hard`.

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
- Tie back to Module 6: the safe-git habits ARE the disaster-recovery plan.
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- "All green, ready to ship" — almost never true after one workshop; be honest.
- Vague next steps ("improve security") instead of one concrete action.
- 4-page reports — one page or it doesn't get read.
- Skipping the verdict entirely.

<!--
SPEAKER NOTES — slide 4 (common mistakes, 30 sec)
Instructor cues:
- Model honesty: mark two axes red live and say why.
-->

---

<!-- _class: tpl-show -->

## Live demo · Score the Notes API (4 min)

1. Pick the Module 4 Notes API.
2. Paste the assessment prompt:

```text
Assess this repo for production readiness across 5 axes: Security, Observability,
Deployment, Runbooks, Rollback. Status per axis + biggest risk + a go/no-go verdict.
```

3. Walk the class through the 5-axis output; mark two red, three amber, none green.
4. State the go / no-go with the smallest next step.

**Success signal**: an honest verdict with one concrete Monday-morning action.

<!--
SPEAKER NOTES — slide 5 (demo, 4 min)
-->

---

<!-- _class: tpl-try -->

## Your turn · Production Readiness Report (8 min)

**Exercise**: [`exercises/part-10/README.md`](../exercises/part-10/README.md)

Pick **one** project from today (likely Module 4) and assess it:

- Run the production-readiness skill against it.
- One page: 5 axes, each with **status · biggest risk · smallest next step**.
- End with a decisive **go / no-go** verdict (≤ 25-word rationale).

**Deliverable**: `module-10/production-readiness-report.md`.

**Success signal**: all five axes covered + an honest verdict + one concrete next step.

<!--
SPEAKER NOTES — slide 6 (hands-on, 8 min)
- Catch "all green" reports — send them back. 2-min warning at the 6-min mark.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] All 5 axes covered.
- [ ] Honest go / no-go verdict with ≤ 25-word rationale.
- [ ] One concrete Monday-morning step.

**Next** — that's the loop, ten times over. We close with Q&A, the exam briefing, and Monday.
**Part 11 — Q&A, Exam Briefing & Next Steps.**

<!--
SPEAKER NOTES — slide 7 (wrap, 1 min)
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (matches Module 1 pilot).
cover -> theory (5 axes) -> reference (overeager agents · mistakes) -> live demo -> your turn -> done.
-->
