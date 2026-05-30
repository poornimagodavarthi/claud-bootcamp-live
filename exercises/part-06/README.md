# Module 6 — Git Workflows for Safe AI Dev

## Goal

Take your module-5 work, branch it, split it into atomic commits whose messages Claude wrote, and ship a real PR description.

## Scenario

Your working tree is dirty with everything from the morning. A senior engineer would never push that as one commit on `main`. Today you do it correctly — and let Claude do the prose work.

## Starter instructions

1. `cd` into your module-5 repo.
2. Confirm `git status` shows the dirty tree.
3. Create `module-06/` for submission artefacts.

## Claude Code prompt to use

```text
COMMIT SPLITTER
Here is the working-tree diff (output of `git diff --staged`).
Propose 3–6 atomic commits. For each: a Conventional Commit subject line
(<= 72 chars) and a body explaining why (not what — the diff shows what).
Then list which paths/hunks belong to which commit so I can split.
```

```text
PR DESCRIPTION
Generate a pull request description from the branch diff below.
Sections, in order:
- Summary (2 sentences)
- Why
- What changed (bullets, grouped by area)
- How to test (exact commands)
- Risk
- Rollback
End with a "Reviewer checklist" of 3–5 yes/no items.
Keep the whole thing under 40 lines.
```

## Manual validation steps

Paste one command at a time (interactive zsh does not treat `#` as a comment):

```bash
git switch -c feat/<your-scope>
git add -A
git diff --staged | pbcopy
git log --oneline
git diff main..HEAD | pbcopy
```

Notes:

- `git diff --staged | pbcopy` copies the staged diff to the clipboard (macOS) — paste it into Claude. On Linux use `xclip -selection clipboard` or `wl-copy`.
- Apply Claude's commit groupings via `git reset` + selective `git add` + `git commit`.
- `git diff main..HEAD | pbcopy` copies the branch diff to paste into Claude for the PR description.

## Expected deliverable

```text
module-06/
├── branch.txt    # branch name + final `git log --oneline` output
├── commits.md    # commit messages Claude proposed and which you accepted/edited
└── pr.md         # final PR description
```

## Definition of done

- [ ] Feature branch named `<type>/<scope>-<summary>`.
- [ ] At least 3 atomic commits with Conventional Commit subjects.
- [ ] `pr.md` has all six required sections + reviewer checklist.
- [ ] Real PR opened or simulated (screenshot acceptable).

## Stretch challenge

Use the `skills/git-workflow/SKILL.md` skill against the same diff and compare its output to the prompt-only output in `module-06/skill-vs-prompt.md`.

**Bonus — `@claude` GitHub Action**: Add the `anthropics/claude-code-action` workflow to your repo (`.github/workflows/claude.yml`) so opening this PR triggers an automated `@claude` review comment. Capture the resulting comment as `module-06/claude-action-review.md`. See `slides/part-06-git-workflows.md` for the wiring snippet.

## Troubleshooting

| Symptom | Fix |
|---|---|
| One giant commit | Re-run the splitter; apply with `git reset` and selective `git add -p`. |
| PR text says *what* but not *why* | Re-prompt with the diff *and* an explicit "explain why" instruction. |
| Pushed to `main` | Reset, branch, force-push to your feature branch only. |
