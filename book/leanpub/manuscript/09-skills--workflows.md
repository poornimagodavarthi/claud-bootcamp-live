# 09. Skills & Workflows

Module 09 · 22 min

## Skills, Hooks, MCP & Multi-Agent

**Stop re-typing workflows. Package them. This is agentic engineering.**

### Theory · Four pillars of agentic engineering (4 min)

1. **Skills** — packaged workflows at `skills/<name>/SKILL.md`, invoked with `/<name>`. Your carry-out from today.
2. **Hooks** — shell commands that fire before/after Claude actions (format, lint, deny dangerous commands).
3. **MCP** — open connectors to issue trackers, docs, chat, internal tools, read as first-class context.
4. **Multi-agent** — a lead agent fans work out to workers in separate worktrees.

> Skills are the unit you'll reuse most. The rest make Claude a teammate, not a chatbot.

### The four power-ups

![Agentic engineering pillars: Skills, Hooks, MCP, Multi-agent](resources/09-skills-catalogue.png)

**Skills · Hooks · MCP · Multi-agent** — Skills are the one you'll reuse most.

### Reference · Hooks & MCP

**Hooks** — `.claude/hooks.json`:

- `post-edit` → `npx prettier --write` (auto-format).
- `pre-bash` → deny `rm -rf` (guardrail).
- `pre-commit` → run tests (no broken commits).

**MCP (Model Context Protocol)** — connect, don't paste:

- Jira / Linear / GitHub · Drive / Notion · Slack.
- **Least privilege**: read scope unless you truly need write.

### Reference · Multi-agent & common mistakes

**Multi-agent fan-out** — lead splits a feature across workers (backend / frontend / tests) in separate worktrees. **Don't** use it for tasks < 30 min, shared mutable state, or non-independent sub-tasks.

**Common mistakes**

- Vague skill body ("do a good job").
- Project-specific paths/versions in a skill (won't carry over).
- Skipping the **Worked example** (reviewers can't tell if it works).
- Fanning out 4 agents on a 10-minute task.

### Live demo · Author a Skill in 4 minutes (5 min)

1. Open `skills/code-review/SKILL.md`; read its H2 headers aloud.
2. Paste the drafting prompt:

```text
Draft a SKILL.md named "score-candidates" using the same H2 sections as
code-review/SKILL.md. Purpose: score 3 diffs on Correctness, Simplicity, Fit.
```

3. Invoke it: `/score-candidates` on three diffs.
4. Observe Claude produce output matching the skill's **Outputs** section.

**Success signal**: the new skill runs and its output matches its own spec — no extra prompting.

### Live demo · Connect GitHub over MCP (4 min)

**"Connect, don't paste."** Let Claude read GitHub directly instead of copying issue text into chat.

1. Add the connector with a **fine-grained, read-scoped** token:

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer $GITHUB_PAT"
```

2. Verify + authenticate: run `/mcp` (status should read **connected**).
3. Ask a question that needs the live repo — paste:

```text
Show me all open PRs assigned to me, then summarize what PR #456 changes.
```

**Success signal**: real PR data Claude could only get by reading the connector — zero copy-paste.

### Your turn · Author a reusable Skill (10 min)

**Exercise**: [`exercises/part-09/README.md`](#hands-on-exercise--module-09)

Write one **project-agnostic** skill for a workflow you'll repeat (e.g. `commit-and-pr`, `screenshot-diff`, `regression-postmortem`):

- Valid frontmatter (`name`, `description`); all **6 H2 sections** in order; body ≤ 80 lines.
- **No** project-specific paths, filenames, or versions.

**Deliverables**: `module-09/skill/SKILL.md` · `module-09/invocation.md` (one real invocation + output).

**Stretch**: add a `hooks.json`, sketch an `mcp-brief.md`, or fan a task out to two sub-agents.

**Success signal**: one real invocation whose output matches the skill's **Outputs** section.

### Done & next (1 min)

**Definition of done**

- [ ] Valid frontmatter; all 6 H2 sections in order; body ≤ 80 lines.
- [ ] No project-specific paths/versions in the body.
- [ ] One real invocation with output matching the **Outputs** spec.

**Next** — we decide if any of today's projects is actually ready to ship.
**Module 10 — Production Readiness.**

## Hands-on exercise — Module 09 {#hands-on-exercise--module-09}

> **Companion repository** — Work this exercise from the live files in the [Claude Code Bootcamp repository](https://github.com/lucab85/Claude-Code-Bootcamp): [`exercises/part-09/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-09/README.md).
> Reference solution: [`exercises/part-09/solution/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-09/solution/README.md).

## Module 9 — Skills, Hooks, MCP & Multi-Agent

### Goal

Turn the Notes API you built in Module 4 into a **repeatable workflow**: author a skill that smoke-tests it, wire a **hook that actually fires** and blocks a broken commit, then run **one scoped MCP action** against GitHub. Every step produces something you can run and check — no abstract write-ups. Multi-agent fan-out is the stretch.

### Scenario

You shipped a Notes API in Module 4 and tested it in Module 5. On Monday a teammate will touch it. You want three guardrails in place: a skill anyone can invoke to verify the API in one command, a pre-commit hook that refuses to let a broken API land, and a GitHub action that files the result — without handing the agent your whole repo. By the end you will have *run* each guardrail and watched it work (and watched the hook reject a bad commit).

### Starter instructions

1. Copy your Module-4 winner into the working folder so the skill has something real to test:
   ```bash
   mkdir -p module-09
   cp ../part-04/solution/python/winner/notes_api.py module-09/   # or your own
   ```
2. Read `skills/code-review/SKILL.md` (skill structure) and `skills/mcp-context-brief/SKILL.md` (how to bound an MCP call).
3. Skim the contract: `specs/001-bootcamp-course-materials/contracts/skill.contract.md`.
4. Work inside `module-09/` from here on.

### Claude Code prompt to use

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

### Manual validation steps

1. Skill is well-formed:
   ```bash
   head -10 module-09/skill/SKILL.md           # YAML frontmatter: name + description
   grep -E '^## ' module-09/skill/SKILL.md      # Purpose · When to use · Body · Inputs · Outputs · Worked example
   ```
2. Skill actually runs and passes against the good API: follow the worked example's bash block and expect `PASS` for all five endpoints and the 404 probe.
3. Hook really blocks: with the bug applied, `git commit` exits non-zero and prints a FAIL line. `module-09/hook-fired.md` shows it.
4. MCP run is scoped: `module-09/mcp-run.md` names exactly one repo, one allowed action, and either a real issue URL or the dry-run tool call.

### Expected deliverable

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

### Definition of done

- [ ] `notes-api-smoke/SKILL.md` has valid frontmatter and all 6 H2 sections in order: Purpose · When to use · Body · Inputs · Outputs · Worked example.
- [ ] The worked example **runs as written** and prints PASS for all five endpoints + the 404 probe — captured in `invocation.md`.
- [ ] Skill body is project-agnostic (path + port are inputs); no hard-coded `module-09` or framework version inside the Body section.
- [ ] `hooks.json` registers a pre-commit hook that runs the skill and **exits non-zero on FAIL**.
- [ ] `hook-fired.md` shows a real blocked commit (FAIL → commit aborted), and the bug was reverted afterward.
- [ ] `mcp-run.md` opens with a ≤5-line brief (one repo, one allowed action, stop condition) and ends with a real issue URL **or** the exact dry-run tool call.

### Stretch challenge

Run the same verification with a **multi-agent fan-out**: a "lead" plus two "worker" agents (or two `git worktree`-isolated agents) each smoke-test a different candidate API, and the lead picks the winner. Capture the comparison as `module-09/multi-agent-compare.md`. Note explicitly when fan-out is **worse** than a single agent — that's the real learning.

### Troubleshooting

| Symptom | Fix |
|---|---|
| Skill body hard-codes `module-09/notes_api.py` | Move the path + port into the Inputs section; keep only the worked example concrete. |
| Worked example "passes" but never started the server | The example must boot the app (`uv run … uvicorn notes_api:app --port 8099 &`), wait for it, then curl. No server = no test. |
| `pip install` / `python3` fails (3.14 pyexpat) | Use `uv run --with fastapi --with uvicorn` everywhere — the skill and the hook. |
| Hook "fires" but commit still succeeds | The hook must `exit 1` on FAIL. Echoing a warning is not blocking. Re-check the exit code. |
| No GitHub MCP server configured | Run the action in dry-run and record the exact tool call + arguments. The point is scoping, not the network round-trip. |
| MCP brief balloons past 5 lines | The task is too big. One repo, one issue, one stop condition. |

## Solution — Module 09 {#solution--module-09}

## Reference solution — Module 9

> **Stop**: only open this after you have authored your own `notes-api-smoke` skill, wired the hook, and run the MCP action.

This module's deliverable is a **runnable bundle** built around the Notes API from Module 4:

```text
module-09/
├── notes_api.py                    # carried over from Module 4 (system under test)
├── skill/
│   └── SKILL.md                    # notes-api-smoke — runnable worked example
├── .claude/
│   └── hooks.json                  # pre-commit hook that runs the skill
├── invocation.md                   # real PASS/FAIL output
├── hook-fired.md                   # proof the hook blocked a broken commit
├── mcp-run.md                      # 5-line brief + real issue URL / dry-run call
└── multi-agent-compare.md          # stretch — fan-out comparison
```

### Reference `SKILL.md` (skeleton — your Body must be project-agnostic)

```markdown
---
name: notes-api-smoke
description: Boot a single-file FastAPI notes app and assert its 5 CRUD endpoints plus the 404 probe, printing PASS/FAIL per check.
---

## Purpose
Verify a notes API is wired correctly in one command, so a teammate can trust
it before building on top.

## When to use
Before committing changes to a notes-style CRUD API, or in a pre-commit hook.

## Body
1. Boot the app under test on the given port.
2. POST a note → expect 201; capture the id.
3. GET /notes and GET /notes/{id} → expect 200.
4. PATCH /notes/{id} → expect 200.
5. DELETE /notes/{id} → expect 204.
6. GET /notes/999 → expect 404.
7. Print `PASS <check>` or `FAIL <check>` per step; exit non-zero on any FAIL.

## Inputs
- module_path: path to the app module (default `notes_api.py`).
- port: free TCP port (default 8099).

## Outputs
- One `PASS`/`FAIL` line per check, then a final `RESULT: PASS|FAIL`.

## Worked example
```bash
PORT=8099
uv run --with fastapi --with uvicorn uvicorn notes_api:app --port "$PORT" &
SRV=$!; sleep 2
fail=0
code=$(curl -s -o /tmp/n.json -w '%{http_code}' -X POST localhost:$PORT/notes \
  -H 'content-type: application/json' -d '{"title":"a","body":"b"}')
[ "$code" = 201 ] && echo "PASS create" || { echo "FAIL create ($code)"; fail=1; }
id=$(sed -n 's/.*"id":\([0-9]*\).*/\1/p' /tmp/n.json)
[ "$(curl -s -o /dev/null -w '%{http_code}' localhost:$PORT/notes)" = 200 ] \
  && echo "PASS list" || { echo "FAIL list"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' localhost:$PORT/notes/$id)" = 200 ] \
  && echo "PASS get" || { echo "FAIL get"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' -X PATCH localhost:$PORT/notes/$id \
  -H 'content-type: application/json' -d '{"title":"z"}')" = 200 ] \
  && echo "PASS patch" || { echo "FAIL patch"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE localhost:$PORT/notes/$id)" = 204 ] \
  && echo "PASS delete" || { echo "FAIL delete"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' localhost:$PORT/notes/999)" = 404 ] \
  && echo "PASS 404" || { echo "FAIL 404"; fail=1; }
kill $SRV
[ "$fail" = 0 ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }
```
```

### Reference `.claude/hooks.json`

```json
{
  "hooks": {
    "pre_commit": [
      {
        "name": "notes-api-smoke",
        "command": "uv run --with fastapi --with uvicorn bash skill/run.sh notes_api.py 8099"
      }
    ]
  }
}
```

The hook **must exit non-zero on FAIL** — that is what blocks the commit. A hook
that only echoes a warning is not a guardrail.

### Reference `hook-fired.md` (what proof looks like)

```text
$ git commit -m "wip"
FAIL list (500)
RESULT: FAIL
husky/pre-commit: hook exited with code 1 — commit aborted
$ git checkout -- notes_api.py    # reverted the injected bug
```

### Reference `mcp-run.md` (5-line brief + result)

```markdown
Task: file the smoke-test result as a GitHub issue.
Server: github (scope: repo acme/notes only).
Allowed: open ONE issue. Forbidden: everything else (no merges, no other repos).
Stop: when the issue is created (capture URL).

Result: opened https://github.com/acme/notes/issues/42
  title: "notes-api-smoke: PASS on 2026-05-30"
# If no MCP server is configured, record the dry-run instead:
# would call: github.create_issue(repo="acme/notes",
#   title="notes-api-smoke: PASS on 2026-05-30", body=<skill output>)
```

### Multi-agent fan-out (stretch)

The reference comparison smoke-tested **three candidate APIs**:
1. Single agent runs the skill against all three in sequence.
2. Lead + 2 workers — each worker tests one candidate, lead picks the winner.
3. Two `git worktree`-isolated agents on competing fixes.

The takeaway captured in `multi-agent-compare.md`: fan-out helps when the checks are
**independent per candidate**; it hurts when the agents must agree on a single shared
verdict and end up re-litigating each other's output.

### Definition of done

See `../README.md`.
