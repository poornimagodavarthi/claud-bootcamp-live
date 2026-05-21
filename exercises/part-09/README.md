# Module 9 — Author Your Own Claude Skill

## Goal

Author a project-agnostic `SKILL.md` that follows the contract, and invoke it on a real input from earlier today.

## Scenario

You've used three or four shipped skills today. Now you author the one *you* will reach for first on Monday. It must work in any repo, not just this one.

## Starter instructions

1. Read `skills/code-review/SKILL.md` end to end. It's the worked example.
2. Read the contract: [`specs/001-bootcamp-course-materials/contracts/skill.contract.md`](../../specs/001-bootcamp-course-materials/contracts/skill.contract.md).
3. Pick a workflow you actually want to repeat (suggestions in the slide deck).
4. Create `module-09/skill/SKILL.md`.

## Claude Code prompt to use

```text
DRAFT THE SKILL
I want a Claude Skill called `<your-name>` that <one-sentence purpose>.
Following the contract at specs/001-bootcamp-course-materials/contracts/skill.contract.md,
draft the SKILL.md. Body must be project-agnostic — no references to specific
filenames or framework versions. Worked example must be runnable as-is.
```

```text
INVOKE THE SKILL
Use the `<your-name>` skill at module-09/skill/SKILL.md.
Inputs: <attach or paste the input>.
Produce the output exactly as the skill's "Outputs" section specifies.
```

## Manual validation steps

1. `head -10 module-09/skill/SKILL.md` shows valid YAML frontmatter with `name` and `description`.
2. `grep -E '^## ' module-09/skill/SKILL.md` lists exactly: Purpose, When to use, Body, Inputs, Outputs, Worked example.
3. `grep -ciE 'this repo|bootcamp|module-0[0-9]|FastAPI|Hono'` returns 0 — no project-specific tokens.
4. The worked example runs as written.

## Expected deliverable

```text
module-09/
├── skill/
│   └── SKILL.md
└── invocation.md   # one real prompt + Claude's output
```

## Definition of done

- [ ] Frontmatter valid: `name`, `description`.
- [ ] All 6 H2 sections present in order: Purpose · When to use · Body · Inputs · Outputs · Worked example.
- [ ] No repo-specific or workshop-specific paths/filenames/versions in the body.
- [ ] One real invocation captured in `invocation.md`.

## Stretch challenge

Take your skill, drop it into a *different* personal repo, invoke it there, and capture the output as `module-09/portability-proof.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Skill body says "do a good job" | Make every instruction operational — name the inputs, the steps, the outputs. |
| Skill mentions `tasks.json` or `notes.db` | Generalise. Skills must carry over. |
| Worked example doesn't run | Replace with one from a real input you used today. |
