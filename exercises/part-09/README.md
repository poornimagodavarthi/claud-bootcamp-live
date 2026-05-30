# Module 9 — Skills, Hooks, MCP & Multi-Agent

## Goal

Turn the Notes API you built in Module 4 into a **repeatable workflow**: author a skill that smoke-tests it, wire a **hook that actually fires** and blocks a broken commit, then run **one scoped MCP action** against GitHub. Every step produces something you can run and check — no abstract write-ups. Multi-agent fan-out is the stretch.

## Scenario

You shipped a Notes API in Module 4 and tested it in Module 5. On Monday a teammate will touch it. You want three guardrails in place: a skill anyone can invoke to verify the API in one command, a pre-commit hook that refuses to let a broken API land, and a GitHub action that files the result — without handing the agent your whole repo. By the end you will have *run* each guardrail and watched it work (and watched the hook reject a bad commit).

## Starter instructions

1. Copy your Module-4 winner into the working folder so the skill has something real to test:
   ```bash
   mkdir -p module-09
   cp ../part-04/solution/python/winner/notes_api.py module-09/   # or your own
   ```
2. Read `skills/code-review/SKILL.md` (skill structure) and `skills/mcp-context-brief/SKILL.md` (how to bound an MCP call).
3. Skim the contract: [`specs/001-bootcamp-course-materials/contracts/skill.contract.md`](../../specs/001-bootcamp-course-materials/contracts/skill.contract.md).
4. Work inside `module-09/` from here on.

## Claude Code prompt to use

```text
AUTHOR A SKILL THAT TESTS REAL CODE
Following specs/001-bootcamp-course-materials/contracts/skill.contract.md,
write module-09/skill/SKILL.md for a skill called `notes-api-smoke`.
Purpose: boot a single-file FastAPI notes app and assert its 5 endpoints
(POST/GET/GET-by-id/PATCH/DELETE) return 201/200/200/200/204 and that
GET /notes/999 returns 404. The Worked example must be a runnable bash
block using `uv run --with fastapi --with uvicorn` + curl, printing PASS
or FAIL per endpoint. Body must be project-agnostic (take the module path
and port as inputs), but the worked example targets module-09/notes_api.py.
```

```text
INVOKE THE SKILL FOR REAL
Use the `notes-api-smoke` skill at module-09/skill/SKILL.md against
module-09/notes_api.py on port 8099. Run it, then paste the actual
PASS/FAIL output into module-09/invocation.md. Do not fabricate results.
```

```text
WIRE A HOOK THAT ACTUALLY FIRES
Create module-09/.claude/hooks.json with one pre-commit hook that runs the
`notes-api-smoke` skill and exits non-zero on any FAIL. Then prove it:
introduce a one-line bug in notes_api.py (e.g. return 500 on GET /notes),
attempt a commit, and show the hook BLOCKING it. Capture the blocked-commit
terminal output in module-09/hook-fired.md, then revert the bug.
```

```text
RUN ONE SCOPED MCP ACTION
Following skills/mcp-context-brief/SKILL.md, write a 5-line brief at the top
of module-09/mcp-run.md (task, server, scope = ONE repo, allowed action =
open one issue, stop condition). Then use the GitHub MCP server to open an
issue titled "notes-api-smoke: <PASS|FAIL> on <date>" with the skill output
as the body. If no GitHub MCP server is configured, run it in dry-run and
record the exact tool call it WOULD make. Append the result to mcp-run.md.
```

## Manual validation steps

1. Skill is well-formed:
   ```bash
   head -10 module-09/skill/SKILL.md           # YAML frontmatter: name + description
   grep -E '^## ' module-09/skill/SKILL.md      # Purpose · When to use · Body · Inputs · Outputs · Worked example
   ```
2. Skill actually runs and passes against the good API: follow the worked example's bash block and expect `PASS` for all five endpoints and the 404 probe.
3. Hook really blocks: with the bug applied, `git commit` exits non-zero and prints a FAIL line. `module-09/hook-fired.md` shows it.
4. MCP run is scoped: `module-09/mcp-run.md` names exactly one repo, one allowed action, and either a real issue URL or the dry-run tool call.

## Expected deliverable

```text
module-09/
├── notes_api.py            # carried over from Module 4 (the system under test)
├── skill/
│   └── SKILL.md            # notes-api-smoke — runnable worked example
├── .claude/
│   └── hooks.json          # one pre-commit hook that runs the skill
├── invocation.md           # real PASS/FAIL output from running the skill
├── hook-fired.md           # terminal proof the hook blocked a broken commit
└── mcp-run.md              # 5-line brief + real issue URL (or dry-run tool call)
```

## Definition of done

- [ ] `notes-api-smoke/SKILL.md` has valid frontmatter and all 6 H2 sections in order: Purpose · When to use · Body · Inputs · Outputs · Worked example.
- [ ] The worked example **runs as written** and prints PASS for all five endpoints + the 404 probe — captured in `invocation.md`.
- [ ] Skill body is project-agnostic (path + port are inputs); no hard-coded `module-09` or framework version inside the Body section.
- [ ] `hooks.json` registers a pre-commit hook that runs the skill and **exits non-zero on FAIL**.
- [ ] `hook-fired.md` shows a real blocked commit (FAIL → commit aborted), and the bug was reverted afterward.
- [ ] `mcp-run.md` opens with a ≤5-line brief (one repo, one allowed action, stop condition) and ends with a real issue URL **or** the exact dry-run tool call.

## Stretch challenge

Run the same verification with a **multi-agent fan-out**: a "lead" plus two "worker" agents (or two `git worktree`-isolated agents) each smoke-test a different candidate API, and the lead picks the winner. Capture the comparison as `module-09/multi-agent-compare.md`. Note explicitly when fan-out is **worse** than a single agent — that's the real learning.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Skill body hard-codes `module-09/notes_api.py` | Move the path + port into the Inputs section; keep only the worked example concrete. |
| Worked example "passes" but never started the server | The example must boot the app (`uv run … uvicorn notes_api:app --port 8099 &`), wait for it, then curl. No server = no test. |
| `pip install` / `python3` fails (3.14 pyexpat) | Use `uv run --with fastapi --with uvicorn` everywhere — the skill and the hook. |
| Hook "fires" but commit still succeeds | The hook must `exit 1` on FAIL. Echoing a warning is not blocking. Re-check the exit code. |
| No GitHub MCP server configured | Run the action in dry-run and record the exact tool call + arguments. The point is scoping, not the network round-trip. |
| MCP brief balloons past 5 lines | The task is too big. One repo, one issue, one stop condition. |
