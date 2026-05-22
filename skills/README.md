# Claude Skills Library

> Reusable Claude Code skills authored for the **Claude Code Bootcamp** by Luca Berton.
> Drop this `skills/` directory into any Claude Code-enabled project and the skills become auto-discoverable.

**Licensed MIT — safe for commercial reuse.** See [`LICENSE`](LICENSE).

## What is a Skill?

A skill is a Markdown file (`SKILL.md`) with YAML frontmatter that Claude Code reads and offers in its skill picker. Each skill packages a reusable prompt, checklist, or workflow.

## The 10 skills

| Skill | Purpose |
|---|---|
| [`claude-md-template`](claude-md-template/SKILL.md) | Generate a project-aware `CLAUDE.md` brain file from your repo. |
| [`code-review`](code-review/SKILL.md) | Run a structured Claude code review on a diff or file. |
| [`test-generation`](test-generation/SKILL.md) | Generate a focused test suite for a target function/module. |
| [`best-of-n`](best-of-n/SKILL.md) | Produce N candidate implementations, score, pick the winner. |
| [`refactor`](refactor/SKILL.md) | Refactor a file or module under explicit constraints. |
| [`release-notes`](release-notes/SKILL.md) | Turn a `git log` range into categorized release notes. |
| [`security-checklist`](security-checklist/SKILL.md) | Scan code against a fixed security checklist. |
| [`git-workflow`](git-workflow/SKILL.md) | Walk through a feature-branch + PR flow with AI-generated commit/PR text. |
| [`documentation-generation`](documentation-generation/SKILL.md) | Generate `README.md`, `ARCHITECTURE.md`, `HANDOFF.md` for a module. |
| [`production-readiness-review`](production-readiness-review/SKILL.md) | Produce a 5-axis production readiness report. |

## How to install

1. Copy this `skills/` directory into the root of your target repo (or a parent repo that Claude Code scans).
2. Open Claude Code in that repo. The skills appear in the skill picker by `name` (declared in each `SKILL.md`'s frontmatter).
3. Invoke a skill by its name; supply the inputs documented in its **Inputs** section.

## How each skill is structured

Every `SKILL.md` follows the same shape, declared by [`specs/001-bootcamp-course-materials/contracts/skill.contract.md`](../specs/001-bootcamp-course-materials/contracts/skill.contract.md):

- **Frontmatter** — `name`, `description` (one-line summary used by the picker)
- **Purpose** — what the skill does
- **When to use** — concrete trigger scenarios
- **Body** — the prompt or checklist Claude actually runs
- **Inputs** — what the user supplies
- **Outputs** — what Claude returns
- **Worked example** — input + expected output sketch

## Project-agnostic guarantee

Every skill in this directory is **path-agnostic**. No skill references the bootcamp repo's layout, project names, or sample data. You can drop the directory into any codebase unchanged.

## Contributing

This directory is part of the [Claude Code Bootcamp](../README.md) materials. Improvements via PR welcome. The skills license (MIT) is decoupled from the course materials license (CC BY-NC-SA 4.0) on purpose — you may re-package the skills inside commercial products without re-licensing the bootcamp content.
