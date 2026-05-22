# Contract — 10-Section Deck Structure (Beginner)

**Feature**: `002-claude-beginner-course`  
**Applies to**: Every Marp deck under `slides/beginner/part-NN-*.md`  
**Enforced by**: `scripts/validate.sh` (extension R3.1)  
**Spec**: FR-010, FR-011, FR-012, FR-013, FR-014, FR-015

---

## Required structure

Every beginner deck MUST contain, in this exact order, the following 10 sections. Sections 2–10 are H2 (`## …`) headings; section 1 is the deck's single H1.

| # | Section | Heading text (exact) | Constraints |
|---|---------|----------------------|-------------|
| 1 | Title slide | (H1 = the module title) | One H1 only; followed by `<!-- _class: lead -->` for the lead-slide layout |
| 2 | What you'll learn | `## What you'll learn` | Exactly 3 bullets, each ≤ 12 words, verb-first ("Install…", "Run…", "Recognize…") |
| 3 | Why this matters | `## Why this matters` | One paragraph + one analogy line. No bullets. |
| 4 | The one concept | `## The one concept` | One bolded term + one-sentence definition. No code. |
| 5 | Show me | `## Show me` | One annotated screenshot OR one fenced code block OR one literal terminal transcript. NO pseudocode. |
| 6 | Try it yourself | `## Try it yourself` | 3–5 numbered steps, each one action. Completable inside the deck (no separate file). |
| 7 | Common mistakes | `## Common mistakes` | ≤ 3 bullets, each one sentence. |
| 8 | Lesson reflection | `## Lesson reflection` | 1–2 italicized prompt questions. |
| 9 | What's next | `## What's next` | One line pointing at the next module by number and slug. |
| 10 | Glossary card | `## Glossary card` | One `**term**: definition` line per new term introduced. Lines MUST match `GLOSSARY.md` byte-for-byte. |

## Frontmatter requirements

```yaml
---
marp: true
theme: default
paginate: true
size: 16:9
title: "<Module NN — Human title>"
description: "<one-line learner-facing summary>"
---

<!-- duration: NN min -->
```

The `<!-- duration: NN min -->` marker MUST appear within the first 30 lines after the frontmatter and MUST match the canonical budget for the module number (20/25/30/25/30/25/25/30 for parts 01–08).

## Density caps

- Content slide count ≤ 12 (between title slide and Glossary card; counted as `---` separators in the deck body).
- Any single slide ≤ 5 bullets.
- Any single fenced code block ≤ 8 lines.

## Prompt copy-paste rule (FR-014)

Every fenced code block tagged as a Claude Code prompt (by a preceding `**Prompt to paste:**` label or by appearing in the "Show me" or "Try it yourself" section) MUST be copy-paste-ready. The validator REJECTS any prompt containing `...` (ellipsis) or `<placeholder>` style angle-bracketed variables, with the single exception of `<your-name>` style learner-substituted values which MUST also appear in the surrounding prose as "(replace `<your-name>` with your actual name)".

## Glossary identity rule (FR-015, SC-006)

Every `**term**: definition` line on the Glossary card slide MUST appear byte-identically (after stripping trailing whitespace) in `GLOSSARY.md`. The validator extracts both sources, diffs them per term, and fails with `<deck-path>:<line>: glossary drift for term '<term>'` on mismatch.

## Sample skeleton

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
title: "Module 01 — Meet Claude Code"
description: "What Claude Code is, how it differs from chat-in-a-browser, and what 'installed and working' looks like."
---

<!-- duration: 20 min -->

# Module 01 — Meet Claude Code
<!-- _class: lead -->

---

## What you'll learn

- Recognize what Claude Code does on your machine
- Verify your install with one command
- Capture your first prompt round-trip

---

## Why this matters

Claude Code is a tool that lives in your terminal, not in a web tab. That one
difference changes how you work with it — and it is the difference this whole
course is going to teach you, one small lesson at a time.

Think of it like a calculator app on your phone vs a calculator built into
the keyboard you're already typing on.

---

## The one concept

**Claude Code** is the official Anthropic command-line tool that brings Claude
into the terminal where your code already lives.

---

## Show me

```text
$ claude --version
@anthropic-ai/claude-code 2.0.7
$ claude
> hello
Hi! I can help you read or edit code in this folder. What are we doing?
```

---

## Try it yourself

1. Open a terminal.
2. Run `claude --version`.
3. Paste the line you see into a file called `first-prompt.txt`.

---

## Common mistakes

- Running `claude --version` from a folder where the `claude` binary isn't on `PATH`.
- Confusing `claude.ai` (the web chat) with `claude` (the CLI we use here).

---

## Lesson reflection

*What did the terminal print? Was that what you expected?*

---

## What's next

Module 02 — Your first conversation: ask Claude Code to do one tiny thing.

---

## Glossary card

- **Claude Code**: The official Anthropic command-line tool that brings Claude into your terminal.
- **CLI**: A program you control by typing commands instead of clicking.
```

## Validator failure modes

| Symptom | Validator output |
|---|---|
| Missing or misordered H2 | `<file>:<line>: deck missing required section '<heading>' at position N` |
| Wrong duration marker | `<file>:1: deck duration marker says NN but FR-030 mandates MM for module K` |
| > 12 content slides | `<file>: deck has K content slides; cap is 12 (FR-013)` |
| Prompt contains `...` | `<file>:<line>: prompt is not copy-paste-ready (contains '...')` |
| Glossary drift | `<file>:<line>: glossary drift for term '<term>' — deck says "…" but GLOSSARY.md says "…"` |
| Frontmatter incomplete | `<file>:1: frontmatter missing required key '<key>'` |
