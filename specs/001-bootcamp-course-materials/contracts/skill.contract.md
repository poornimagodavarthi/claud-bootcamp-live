# Skill Contract

**Audience**: authors of `skills/<skill-name>/SKILL.md`; reviewers; `scripts/validate.sh`.
**Source rules**: Constitution Principle II; spec FR-016, FR-017, FR-018; research R2.

A "skill" is a Claude Code-native, drop-in artifact that graduates can
reuse in any Claude Code-enabled project. There are exactly **10**
skills. Module 9's deliverable IS this directory (per spec assumption).

## Directory layout

```
skills/
├── LICENSE                                 # MIT (FR-005a)
├── claude-md-template/SKILL.md
├── code-review/SKILL.md
├── test-generation/SKILL.md
├── best-of-n/SKILL.md
├── refactor/SKILL.md
├── release-notes/SKILL.md
├── security-checklist/SKILL.md
├── git-workflow/SKILL.md
├── documentation-generation/SKILL.md
└── production-readiness-review/SKILL.md
```

Directory names MUST match the table above exactly (kebab-case,
lowercase). No alternate names allowed.

## File: `SKILL.md`

Every skill directory MUST contain exactly one file named `SKILL.md`
(uppercase as shown). No `README.md`, `index.md`, or other variants
serve as the skill body.

## Required frontmatter

The file MUST begin with a YAML frontmatter block:

```yaml
---
name: <kebab-name matching the directory>
description: <one-line, ≤120 characters, action-oriented; appears in Claude Code's skill picker>
---
```

- `name` MUST equal the parent directory name.
- `description` MUST be a single line, ≤ 120 characters, starting with
  a verb ("Generate…", "Run…", "Review…", "Refactor…").
- No additional frontmatter fields are required for v1. Authors MAY
  NOT add fields that affect Claude Code matching unless documented in
  a follow-up amendment to this contract.

## Required body sections (6, in order)

After the frontmatter, the body uses these H2 sections in this exact
order:

| # | Heading | Content |
|---|---|---|
| 1 | `## Purpose` | What this skill does, in 1–3 sentences. |
| 2 | `## When to use it` | Concrete trigger situations. ≥ 3 bullets. |
| 3 | `## Prompt body` | The reusable prompt itself, in a fenced ```` ```text ```` block. This is what Claude Code executes. |
| 4 | `## Expected inputs` | What the user/Claude needs to provide (paths, diff scope, target file, etc.). Bulleted. |
| 5 | `## Expected outputs` | What the skill produces (files, comments, summaries, scores). Bulleted. |
| 6 | `## Worked example` | At least one reproducible example: the input scenario, the literal prompt invocation, and an excerpt of the expected output. |

`scripts/validate.sh` checks for **presence in order** of these 6
H2 sections.

## Project-agnostic rule (FR-018)

No `SKILL.md` body or its `## Prompt body` block MAY reference
bootcamp-specific paths or assumptions. Specifically forbidden:

- Mentions of `exercises/part-NN/`, `slides/`, the workshop schedule,
  or the bootcamp itself.
- Hard-coded module names ("CLI Task Manager", "Notes App API", etc.).
- Author/instructor names inside the prompt body.

The `## Worked example` section MAY mention small fictional projects
(e.g., "a small Flask app at `./api/`") but NOT bootcamp paths.

## The 10 required skills

| # | `name` | One-line purpose |
|---|---|---|
| 1 | `claude-md-template` | Generate a high-quality CLAUDE.md tailored to a target project |
| 2 | `code-review` | Review a diff or file against a rubric and surface unsafe AI output |
| 3 | `test-generation` | Generate a meaningful test suite for a target file or function |
| 4 | `best-of-n` | Run a Best-of-N solution-comparison workflow with a tradeoff matrix |
| 5 | `refactor` | Refactor with stated constraints; preserve behavior; emit a diff plan |
| 6 | `release-notes` | Produce release notes from a commit range or PR list |
| 7 | `security-checklist` | Run a security review on a project or diff against the OWASP Top 10 |
| 8 | `git-workflow` | Drive a safe AI-dev Git flow (branch, commit, diff review, PR) |
| 9 | `documentation-generation` | Generate onboarding/handoff docs from a codebase |
| 10 | `production-readiness-review` | Run the full production-readiness review |

## Acceptance test (manual, per skill)

1. Directory name matches the table.
2. `SKILL.md` exists.
3. Frontmatter has `name` and `description`; `name` == directory name;
   `description` ≤ 120 chars and verb-led.
4. All 6 required H2 sections present in order.
5. Section 3 (`## Prompt body`) contains a fenced ```` ```text ```` block.
6. Section 6 (`## Worked example`) is reproducible (a third party can
   follow it).
7. No bootcamp-specific path references anywhere in the file.
8. Validator script reports the skill as VALID.
