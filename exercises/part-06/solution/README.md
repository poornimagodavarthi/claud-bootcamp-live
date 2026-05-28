# Reference solution — Module 6

> **Stop**: only open this after you have split your dirty tree into atomic commits and drafted `pr.md`.

This module produces a **branch history + PR description**, not running code. The reference solution is a worked example of what a strong submission contains.

```text
module-06/
├── branch.txt                    # branch name + final `git log --oneline` output
├── commits.md                    # commits Claude proposed and which you kept/edited
├── pr.md                         # final PR description (six sections + reviewer checklist)
└── claude-action-review.md       # bonus — comment from the @claude GitHub Action
```

## Reference branch shape

```text
feat/task-validation-cleanup
* a1b2c3d  feat(cli): reject empty task titles with exit code 2
* b2c3d4e  refactor(persistence): extract tasks.json read/write into store.py
* c3d4e5f  test(cli): cover delete with missing id
* d4e5f6g  docs(readme): document --help output
```

Four atomic commits. Each Conventional Commit; subject ≤ 72 chars; body explains **why** (the diff shows **what**).

## Reference `pr.md` shape

Six H2 sections in this order: **Summary · Why · What changed · How to test · Risk · Rollback**. Reviewer checklist of 3–5 yes/no items. Whole document ≤ 40 lines.

## `@claude` GitHub Action (bonus)

Wiring snippet (full version in `slides/part-06-git-workflows.md`):

```yaml
# .github/workflows/claude.yml
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

`claude-action-review.md` should be the Markdown comment the Action posted on your PR.

## Definition of done

See `../README.md`. Three or more atomic commits + PR with six sections + reviewer checklist.
