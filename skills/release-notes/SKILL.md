---
name: release-notes
description: Produce formatted release notes from a commit range or PR list, grouped by type and written for end users.
---

## Purpose

Reads a git commit range or a list of pull requests and produces
structured release notes grouped by feature, fix, and breaking change —
written for the audience that will read the changelog, not the engineers
who wrote the code.

## When to use it

- When cutting a release and a changelog or GitHub release body is needed.
- After a sprint to summarise what shipped for stakeholders or users.
- When a PR description needs to double as a customer-facing release note.
- Before publishing a versioned package to communicate what changed.

## Prompt body

```text
Generate release notes for the following range:

SOURCE: SOURCE (a git range like v1.2.0..HEAD, or a list of PR titles/descriptions)
VERSION: VERSION_NUMBER
AUDIENCE: AUDIENCE (default: "end users"; options: "engineers", "end users", "stakeholders")

Steps:
1. Read all commits or PR descriptions in SOURCE.
2. Classify each change as: Feature, Fix, Breaking Change, or Internal (skip Internal in output).
3. Write one bullet per change. Lead with a verb. Write for AUDIENCE — no internal jargon, no ticket numbers.
4. Group bullets under these headings (omit empty groups):
   ## Breaking Changes
   ## New Features
   ## Bug Fixes
5. Add a one-sentence summary at the top: what this release is about.
6. If a breaking change exists, add a "Migration" section with concrete upgrade steps.
```

## Expected inputs

- `SOURCE` — a git range (e.g. `v1.0.0..HEAD`) or a pasted list of PR titles/bodies.
- `VERSION_NUMBER` — the release version string (e.g. `v1.3.0`).
- `AUDIENCE` — who will read the notes (`end users`, `engineers`, or `stakeholders`). Default: `end users`.

## Expected outputs

- A Markdown release notes document with a summary line and grouped sections.
- One bullet per shipped change, written for the specified audience.
- A `## Migration` section if any breaking changes are present.

## Worked example

**Scenario:** Generate release notes for a small API from the last 5 commits.

**Invocation:**
```
/release-notes SOURCE=v1.0.0..HEAD VERSION_NUMBER=v1.1.0 AUDIENCE=end users
```

**Expected output:**
```markdown
## v1.1.0

This release adds search to the notes list and fixes two data-loss bugs.

## New Features
- Search notes by keyword using `GET /notes?q=<term>`.

## Bug Fixes
- Fix missing date values in the recent-items panel.
- Fix PATCH with no fields incorrectly updating the modification timestamp.
```
