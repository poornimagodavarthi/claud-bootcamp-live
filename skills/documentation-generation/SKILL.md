---
name: documentation-generation
description: Generate onboarding and handoff documentation from a codebase, including architecture diagram, component descriptions, and known limitations.
---

## Purpose

Reads a codebase and produces structured documentation — an ASCII
architecture diagram, per-component descriptions, a known-limitations
list, and a handoff section — so a new engineer or AI assistant can
orient quickly without reading all the source.

## When to use it

- Before handing off a project to a new engineer or team.
- When a codebase has grown but documentation hasn't kept pace.
- When onboarding an AI assistant that needs codebase context beyond CLAUDE.md.
- After a significant refactor that made existing docs inaccurate.

## Prompt body

```text
Generate documentation for the project at PROJECT_PATH.

Steps:
1. List all source files and directories. Identify the main entry point(s).
2. Identify the major components (modules, services, classes, route groups).
3. Trace the primary data flow from input to output.

Produce a document with these sections:

## Architecture
An ASCII diagram (using only +, -, |, > characters) showing components and
data flow. No box-drawing Unicode.

## Components
One paragraph per component: purpose, inputs, outputs.

## Data flow
2–4 sentences describing how a typical request or operation moves through the system.

## Known limitations
A bulleted list of up to 5 concrete limitations visible in the code
(not generic advice). Each bullet names a specific file or function.

## Handoff notes
3–5 bullets a new engineer must know before touching this code:
gotchas, implicit contracts, or things that are easy to break silently.
```

## Expected inputs

- `PROJECT_PATH` — the root directory of the project to document (default: current working directory).
- Optionally: a target output filename (default: `ARCHITECTURE.md`).

## Expected outputs

- A Markdown document written to `PROJECT_PATH/ARCHITECTURE.md`.
- Sections: Architecture, Components, Data flow, Known limitations, Handoff notes.

## Worked example

**Scenario:** Document a single-file pricing module.

**Invocation:**
```
/documentation-generation PROJECT_PATH=./pricing
```

**Expected output (excerpt):**
```markdown
## Architecture

caller
  |  items, country, customer
  v
+---------------------------+
|  calc()                   |
|  +----------+  +--------+ |
|  | Item loop|->|Discounts| |
|  +----+-----+  +--------+ |
|       | subtotal           |
|  +----+-----+  +--------+ |
|  | Tax lookup|->|TAX_RATES| |
|  +----+-----+  +--------+ |
+---------------------------+

## Known limitations
- Unknown coupons silently apply no discount (pricing.py:18).
- Negative unit prices are dropped without raising an error (pricing.py:12).
```
