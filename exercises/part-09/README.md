# Module 9 — Skills, Hooks, MCP & Multi-Agent

## Goal

Author a project-agnostic `SKILL.md` that follows the contract, register **one hook** in a local `.claude/hooks.json`, and stage an **MCP** context brief for a connector (Jira / Slack / GitHub). Optionally, fan out a **multi-agent** run for the same task and compare the outputs.

## Scenario

You've used three or four bundled skills today. Now you author the one *you* will reach for first on Monday, surround it with a deterministic hook, and prove you can scope an MCP-mediated action without slurping the whole workspace. Multi-agent fan-out is the stretch.

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

```text
REGISTER A HOOK
Create module-09/hooks.json with a single hook entry. Use one of:
- pre-bash: refuse `rm -rf` outside a worktree
- post-edit: run `npm test` after any file in src/ changes
- pre-commit: run the `code-review` skill on the staged diff
Return the JSON only.
```

```text
PREPARE AN MCP CONTEXT BRIEF
Following skills/mcp-context-brief/SKILL.md, draft module-09/mcp-brief.md
for ONE connector (Jira / Slack / GitHub / Drive). State the task,
the allowed actions, the forbidden actions, and the stop conditions.
Keep it under 400 words.
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
├── hooks.json          # one entry: pre-bash / post-edit / pre-commit
├── mcp-brief.md        # context brief for one MCP connector
└── invocation.md       # one real prompt + Claude's output
```

## Definition of done

- [ ] Frontmatter valid: `name`, `description`.
- [ ] All 6 H2 sections present in order: Purpose · When to use · Body · Inputs · Outputs · Worked example.
- [ ] No repo-specific or workshop-specific paths/filenames/versions in the body.
- [ ] One real invocation captured in `invocation.md`.
- [ ] `hooks.json` registers at least one hook (pre-bash / post-edit / pre-commit) with a non-trivial command.
- [ ] `mcp-brief.md` follows the `mcp-context-brief` skill template; declares allowed actions, forbidden actions, and stop conditions.

## Stretch challenge

Run the same task with a **multi-agent fan-out**: spawn a "lead" plus two "worker" agents (or two `git worktree`-isolated agents) and compare diffs. Capture the comparison as `module-09/multi-agent-compare.md`. Note explicitly when fan-out is **worse** than a single agent — that's the real learning.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Skill body says "do a good job" | Make every instruction operational — name the inputs, the steps, the outputs. |
| Skill mentions `tasks.json` or `notes.db` | Generalise. Skills must carry over. |
| Worked example doesn't run | Replace with one from a real input you used today. |
