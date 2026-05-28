---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 06'
paginate: true
size: 16:9
title: "Module 6 — Git Workflows for Safe AI Dev"
description: "Branch, commit, and PR your AI-generated code safely. Have Claude write the commit message and PR description."
---

<!-- duration: 22 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 06 · 22 min</span>

# Git Workflows for Safe AI Dev

**Never let Claude push to main. Branch, commit atomically, PR — you stay the gate.**

<img class="hero-icon" src="themes/icons/folder.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "Claude can write great commits and PRs — from the diff, not the prompt."
-->

---

<!-- _class: tpl-objectives -->

## Theory · Safe git for AI code (4 min)

- **Branch first**, always: `<type>/<scope>-<summary>` → `feat/notes-api-search`.
- **Atomic commits** — one logical change each. Claude can split a dirty tree if you ask.
- **Conventional Commits**: `feat:` · `fix:` · `chore:` · `docs:` · `test:`.
- **PR description shape**: What changed · Why · How to test · Risk · Rollback.

> Claude writes the commit messages and PR — but **from the actual diff**, never from your prompt.

Full reference: [`skills/git-workflow/SKILL.md`](../skills/git-workflow/SKILL.md).

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- "From the diff, not the prompt" — say it. PRs written from prompts lie about what shipped.
-->

---

<!-- _class: tpl-show -->

## Branch → atomic commits → PR

![Git flow: branch first, atomic Conventional commits, then a PR](intermediate/assets/06-git-flow.svg)

Branch first · **atomic Conventional commits** · PR explains What · Why · Test · Risk · Rollback.

<!--
SPEAKER NOTES — slide 3 (diagram, 1 min)
- Trace left to right; every commit is one logical change.
-->

---

<!-- _class: tpl-show -->

## Reference · Bonus · @claude GitHub Action

`anthropics/claude-code-action` turns Claude into a **teammate in your repo**:

- Mention `@claude` in an issue or PR comment → it proposes a fix.
- Automated PR review on every push.
- Issue-to-PR flow: describe the bug, get a draft PR.

```yaml
# .github/workflows/claude.yml (sketch)
uses: anthropics/claude-code-action@v1
with:
  anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Stretch goal in the exercise — wire it on a throwaway repo.

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
- Optional. Only the fast finishers wire the Action; everyone hears it exists.
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- One giant commit called `feat: stuff` — re-run the splitter.
- PR that says *what* but not *why* — reviewers reject it.
- Writing the PR from the prompt instead of the diff.
- Pushing to main (always branch first).

<!--
SPEAKER NOTES — slide 4 (common mistakes, 30 sec)
Instructor cues:
- Demo on a dirty working tree so the commit-splitter has something to do.
-->

---

<!-- _class: tpl-show -->

## Live demo · Split commits, write the PR (5 min)

1. On the Module 5 tree (dirty): `git switch -c feat/notes-api-tests-and-fixes`. Then paste:

```text
Group these staged changes into atomic commits using Conventional Commit
subjects. Show the plan (files per commit + message) before committing.
```

2. Apply and commit. Then paste:

```text
Write a PR description from the branch diff: What, Why, How to test, Risk, Rollback.
```

3. Review, edit, open a draft PR (or simulate).

**Success signal**: ≥ 3 atomic commits with Conventional subjects; PR explains *why*, not just *what*.

<!--
SPEAKER NOTES — slide 5 (demo, 5 min)
-->

---

<!-- _class: tpl-try -->

## Your turn · Branch → commits → PR (10 min)

**Exercise**: [`exercises/part-06/README.md`](../exercises/part-06/README.md)

Take your Module 5 work onto a feature branch and ship a clean history:

- Create a feature branch; ask Claude to split into **≥ 3 atomic commits**.
- Generate a PR description from the **diff** (What · Why · How to test · Risk · Rollback).

**Deliverables**: `branch.txt` (name + `git log --oneline`) · `commits.md` · `pr.md`.

**Success signal**: a mergeable PR with sensible Conventional-Commit messages.

<!--
SPEAKER NOTES — slide 6 (hands-on, 10 min)
- Watch for one-commit submissions — send them back to the splitter. 3-min warning.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] Feature branch holds all Module 5 work.
- [ ] ≥ 3 atomic commits with Conventional subjects.
- [ ] `pr.md` has all sections: Summary · Why · What changed · How to test · Risk · Rollback.

**Next** — code is safe in git. Now we feed Claude a *picture* and build a UI.
**Module 7 — Multimodal: Screenshot to UI.**

<!--
SPEAKER NOTES — slide 7 (wrap, 1 min)
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (matches Module 1 pilot).
cover -> theory (safe git) -> reference (@claude Action · mistakes) -> live demo -> your turn -> done.
-->
