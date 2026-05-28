# Reference solution — Module 9

> **Stop**: only open this after you have authored your own `SKILL.md`, `hooks.json`, and `mcp-brief.md`.

This module's deliverable is a **bundle of four artefacts**:

```text
module-09/
├── skill/
│   └── SKILL.md                    # your authored skill
├── hooks.json                      # one hook entry
├── mcp-brief.md                    # context brief for one MCP connector
├── invocation.md                   # one real invocation of your skill
└── multi-agent-compare.md          # stretch — fan-out comparison
```

## Reference `SKILL.md` (skeleton — your version must be project-agnostic)

```markdown
---
name: standup-summary
description: Roll up yesterday's commits and today's open PRs into a 3-bullet standup line.
---

## Purpose
Produce one Slack-ready paragraph summarising what changed and what's blocked.

## When to use
At standup time, when you have a noisy commit log and need a 30-second readout.

## Body
1. Run `git log --since=yesterday --pretty=format:"%h %s"`.
2. List open PRs assigned to you via the GitHub MCP connector (read-only).
3. Synthesise into exactly three bullets: shipped, in flight, blocked.

## Inputs
- repo: a git working tree.
- mcp: github connector (scope: PRs assigned to me).

## Outputs
- A Markdown block with three `- ` bullets, no preamble.

## Worked example
[ … ]
```

## Reference `hooks.json`

```json
{
  "hooks": {
    "pre_commit": [
      {
        "name": "code-review-skill",
        "command": "claude skill code-review --input staged-diff"
      }
    ]
  }
}
```

## Reference `mcp-brief.md` (skeleton)

```markdown
# MCP context brief — GitHub connector

Task: triage open PRs in the `backend` repo and post a summary comment to Slack.

Allowed actions:
- Read PRs in github.com/acme/backend (state: open).
- Post one comment to slack channel #eng-standup.

Forbidden actions:
- Merge PRs.
- Open new PRs.
- Read any other repo.

Stop conditions:
- When 3 PRs have been summarised, or
- When the slack comment has been posted.
```

## Multi-agent fan-out (stretch)

The reference comparison ran the same skill via:
1. Single agent.
2. Lead + 2 workers (each on a separate file).
3. Two `git worktree`-isolated agents on the same task.

The takeaway captured in `multi-agent-compare.md`: fan-out helps when the task is **embarrassingly parallel by file**; it hurts when agents need to coordinate.

## Definition of done

See `../README.md`.
