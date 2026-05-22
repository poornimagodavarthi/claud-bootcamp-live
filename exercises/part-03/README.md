# Module 3 — Project Context with CLAUDE.md

## Goal

Author a `CLAUDE.md` for a real repo and prove Claude follows it on the next prompt.

## Scenario

You inherit a repo. Every time you prompt Claude, you re-explain stack, conventions, and "do nots". That waste is what `CLAUDE.md` exists to remove. Today you commit one — and earn it back.

## Starter instructions

1. Pick a repo: your module-2 work, or any personal repo you trust to commit to.
2. `cd` into it.
3. Create `module-03/` in your submission directory.
4. Open `skills/claude-md-template/SKILL.md` for the template.

## Claude Code prompt to use

```text
You are drafting CLAUDE.md for the repo at the current working directory.
Read the repo first. Then propose a CLAUDE.md with these sections:

# Stack       — languages, package managers, runtime versions
# Conventions — naming, file layout, lint/format rules
# Commands    — exact commands for build, test, run, lint
# Do-not      — things you must never do (e.g., add deps without asking)
# Glossary    — domain terms only this team uses

Each line must change your behavior on a future prompt. If a line is just
documentation, omit it. Keep the whole file under 80 lines.
```

## Manual validation steps

1. `wc -l CLAUDE.md` → ≤ 80.
2. Confirm all five H1 sections present: `Stack`, `Conventions`, `Commands`, `Do-not`, `Glossary`.
3. Open a fresh Claude Code chat. Ask one prompt that depends on a `Conventions` line (e.g., naming).
4. Verify Claude obeys.
5. Screenshot the obedient response → `module-03/proof.png`.

## Expected deliverable

```text
module-03/
├── CLAUDE.md      # copy of the file you committed to the underlying repo
└── proof.png      # screenshot of Claude obeying one convention
```

## Definition of done

- [ ] File is committed to the underlying repo (not just sitting in the submission folder).
- [ ] All five H1 sections present.
- [ ] ≤ 80 lines total.
- [ ] `proof.png` shows Claude obeying.
- [ ] You can name one line you deleted in the trim test, and why.

## Stretch challenge

Apply the trim test rigorously: delete each section in turn, re-prompt, observe drift. Document which section caused the largest behavior regression in `module-03/trim-notes.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| File over 80 lines | Trim ruthlessly — every line must change behavior. |
| Claude ignores the file | Confirm it's at repo root and you're in a fresh chat. |
| Proof screenshot is unconvincing | Re-pick a convention that produces a visible diff in output. |
