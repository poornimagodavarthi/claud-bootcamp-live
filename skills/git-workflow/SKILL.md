---
name: git-workflow
description: Drive a safe AI-assisted Git flow — branch, implement, diff review, commit, and open a pull request.
---

## Purpose

Guides an AI-assisted development session through a complete, safe Git
workflow: creating a branch, making changes, reviewing the diff before
committing, writing a Conventional Commit message, and opening a pull
request with a structured description.

## When to use it

- At the start of any feature or fix session to ensure work lands on its own branch.
- Before committing to catch accidental changes, debug code, or secrets in the diff.
- When a PR needs a structured description derived from the actual changes made.
- As a checklist to verify CI-sensitive files weren't accidentally modified.

## Prompt body

```text
Run the safe AI-dev Git workflow for this session.

BRANCH_NAME: BRANCH_NAME (e.g. feat/add-search)
BASE_BRANCH: BASE_BRANCH (default: main)

Steps:
1. Create and switch to BRANCH_NAME from BASE_BRANCH.
2. Implement the requested changes (caller describes the task separately).
3. Before staging, run `git diff` and review it line by line:
   - Flag any debug code, commented-out blocks, or secrets.
   - Flag any files changed that were NOT part of the stated task.
   - Do not proceed until the diff is clean.
4. Stage only the files relevant to the task (no `git add .`).
5. Write a Conventional Commit subject line (≤72 chars) and a body explaining WHY.
   Format: `type(scope): subject\n\nbody`
6. Commit. If a pre-commit hook fails, fix the issue and create a NEW commit — never --amend a published commit.
7. Open a PR against BASE_BRANCH with:
   ## Summary (3 bullets max)
   ## Test plan (checklist)
```

## Expected inputs

- `BRANCH_NAME` — the name for the new branch (e.g. `fix/null-check`).
- `BASE_BRANCH` — the branch to branch from and PR into (default: `main`).
- The task description — what changes should be made (provided by the caller alongside the skill invocation).

## Expected outputs

- A new branch with clean, staged commits.
- A Conventional Commit message with subject and body.
- An opened PR with summary and test-plan sections.

## Worked example

**Scenario:** Add a search endpoint to a notes API.

**Invocation:**
```
/git-workflow BRANCH_NAME=feat/notes-search BASE_BRANCH=main
```

**Expected output (excerpt):**
```
Switched to branch feat/notes-search

[diff review]
+ GET /notes?q=<term> added — looks clean, no debug code.
No unintended files changed.

Commit message:
  feat(notes): add keyword search to GET /notes

  Allows clients to filter notes by title or body via ?q=.
  Implemented with a LIKE query; metacharacters escaped.

PR opened: https://github.com/org/repo/pull/42
```
