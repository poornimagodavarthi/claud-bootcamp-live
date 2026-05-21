# Contract — `scripts/validate.sh` Beginner Extensions

**Feature**: `002-claude-beginner-course`  
**Applies to**: `scripts/validate.sh` (in-place extension)  
**Spec**: FR-051, FR-055, SC-005, SC-006, SC-008  
**Sources**: research.md §R3

---

## Invocation

Unchanged for the intermediate course:

```text
scripts/validate.sh
```

Exit `0` if all checks pass. Exit `1` on any failure. Output format unchanged (`ok: <subject>` or `fail: <file>:<line>: <reason>`).

## Activation

All beginner checks are wrapped in `if [[ -d slides/beginner ]]; then … fi` so the intermediate-only test surface still passes if the beginner course is removed or moved.

## Reuse from existing validator

| Reused element | How |
|---|---|
| HTML-comment stripping pre-pass | `perl -0777 -pe 's/<!--.*?-->//gs'` runs once over each authoring file before regex scans. |
| `STRICT_REGEX` (TODO/TBD/FIXME/XXX) | Applied to all beginner files in addition to intermediate files. |
| `LOOSE_REGEX` (motivational filler) | Same. |
| Parallel-array iteration pattern | New `BEG_DECK_SLUGS` + `BEG_DECK_MINS` arrays follow the existing `DECK_SLUGS`/`DECK_MINS` shape. |
| SKILL.md 6-section check | Applied to `skills/beginner/**/SKILL.md` when the dir exists. |

## New checks (each emits exactly one `ok:` or one `fail:` per item)

### V1. Beginner deck section structure (per `contracts/deck-10-section.md`)

For each `slides/beginner/part-*.md`:
- Extract all H2 headings in document order.
- Assert the list equals exactly: `["What you'll learn", "Why this matters", "The one concept", "Show me", "Try it yourself", "Common mistakes", "Lesson reflection", "What's next", "Glossary card"]`.
- On mismatch: `fail: <file>:<line>: deck H2 sequence mismatch (expected '<expected>' at position N, got '<actual>')`.

### V2. Beginner deck duration marker

For each deck:
- Find `<!-- duration: NN min -->` in the first 30 lines after frontmatter.
- Assert `NN` matches the canonical value from `BEG_DECK_MINS` for that part number (20/25/30/25/30/25/25/30 for parts 01–08).
- On mismatch: `fail: <file>:<line>: duration says NN min, FR-030 requires MM min for module K`.

### V3. Beginner deck content-slide cap (FR-013)

For each deck:
- Count `^---$` separators between the line after the title slide and the `## Glossary card` heading.
- Assert count ≤ 12.
- On overage: `fail: <file>: K content slides exceed cap of 12`.

### V4. Beginner exercise section structure (per `contracts/exercise-7-section.md`)

For each `exercises/beginner/part-*/README.md`:
- Extract all H2 headings in document order.
- Assert the list equals exactly: `["What you'll build", "Before you start", "Step-by-step", "The prompt to paste", "How to know it worked", "If something went wrong", "You did it!"]`.
- On mismatch: same format as V1.

### V5. Beginner exercise scaffolding (FR-022, FR-023)

For each `exercises/beginner/part-NN/` (excluding `module-00-setup`):
- Assert `starter/` exists and `find starter -type f` returns ≥ 1.
- Assert `solution/` exists and `find solution -type f -not -empty` returns ≥ 1.
- On failure: `fail: exercises/beginner/part-NN/: required directory '<starter|solution>' missing or empty`.

For `exercises/beginner/module-00-setup/`:
- Assert `starter/` exists; no `solution/` required.

### V6. Forbidden-tokens regex (FR-055)

Add these globs to the existing forbidden-tokens scan loop:
- `slides/beginner/**/*.md`
- `exercises/beginner/**/*.md`
- `assessments/beginner/**/*.md`
- `GLOSSARY.md`
- `beginner-student-guide.md`
- `beginner-instructor-guide.md`
- `beginner-certificate-template.md`

STRICT and LOOSE regexes are unchanged.

### V7. Beginner duration sum (SC-008)

- Sum the 8 `BEG_DECK_MINS` values.
- Assert `200 ≤ sum ≤ 240`.
- On failure: `fail: beginner module duration sum = N (must be 200..240)`.

### V8. Glossary character-identity (per `contracts/glossary-identity.md`, SC-006)

- Extract `(term, definition)` pairs from every deck's `## Glossary card` section and from `GLOSSARY.md`.
- For each deck pair: assert the same term exists in `GLOSSARY.md` with a byte-identical definition. Failures per `contracts/glossary-identity.md`.
- Assert every `GLOSSARY.md` entry is referenced by ≥ 1 deck (orphan check). On failure: `fail: GLOSSARY.md:<line>: orphan term '<term>' not referenced by any deck`.
- Assert all `GLOSSARY.md` terms are unique. On dup: `fail: GLOSSARY.md:<line>: duplicate term '<term>'`.

### V9. Beginner quiz coverage (FR-040)

Against `assessments/beginner/quiz.md`:
- Count questions (numbered list items at H2 or H3 boundary, format `### Q<N>. …`); MUST be exactly 16.
- For each question, find the preceding `<!-- module: NN -->` HTML comment; group by `NN`.
- Assert each of modules 1..8 has exactly 2 questions.
- Assert each question has exactly 4 options labeled `A.`, `B.`, `C.`, `D.`.
- For each question number, assert `assessments/beginner/answer-key.md` has a matching numbered entry with letter in `{A,B,C,D}`.
- Failures: `fail: assessments/beginner/quiz.md:<line>: <reason>` or `fail: assessments/beginner/answer-key.md:<line>: <reason>`.

### V10. Cross-references (FR-054)

- Assert `README.md` contains a literal link to `beginner-student-guide.md` and to `slides/beginner/README.md`.
- Assert `beginner-student-guide.md` contains a link to `assessments/beginner/quiz.md`, to `beginner-certificate-template.md`, and to `scripts/check-beginner-capstone.sh`.
- Assert `beginner-instructor-guide.md` contains a link to `beginner-student-guide.md`.
- Failures: `fail: <file>: missing required cross-reference to '<target>'`.

### V11. Beginner skills (optional, per FR-060 and Clarifications Q5)

- If `skills/beginner/` does NOT exist: emit `ok: skills/beginner (optional, none authored)`.
- If it exists and contains ≥ 1 `SKILL.md`: apply the existing 6-section SKILL contract to each. Emit one `ok:` or `fail:` per file. Never fail on count (no min, no max).

### V12. Certificate template (FR-043, FR-046)

Against `beginner-certificate-template.md`:
- Extract placeholders matching `\{\{[A-Z_]+\}\}`.
- Assert the set is a superset of `{STUDENT_NAME, COMPLETION_DATE, INSTRUCTOR_NAME, WORKSHOP_TITLE, VERIFICATION_TOKEN}`.
- Failure: `fail: beginner-certificate-template.md: missing required placeholder '{{<NAME>}}'`.

### V13. "Show me" slide contains real evidence (FR-012)

For each beginner deck under `slides/beginner/part-*.md`:
- After HTML-comment stripping, locate the slide body between the line `## Show me` and the next slide separator (`---` on its own line or end-of-file).
- Assert the body contains at least one of:
  - a fenced code block (a line matching `^\`\`\`` opens it, a later line matching `^\`\`\`` closes it), OR
  - a Markdown image link matching `!\[[^\]]*\]\([^)]+\)`.
- Emit `ok: <file>: "Show me" slide has runnable code or screenshot`.
- Failure: `fail: <file>: "Show me" slide must contain a fenced code block or image (no decorative stock imagery)`.
- Rationale: machine-enforces FR-012 so reviewers don't have to catch decorative-only "Show me" slides during PR review.

## Performance budget

The beginner extensions MUST add ≤ 3 seconds to the total validator runtime on a clean checkout. Current intermediate-only run is ~1.5 s; target with beginner extensions is ≤ 5 s.

## Backward compatibility

- No existing intermediate-course check is modified.
- No existing output format changes.
- Exit code semantics unchanged: 0 = all ok, 1 = any failure.
- Removing `slides/beginner/` makes all V* checks become no-ops via the activation gate.

## Test surface for this contract

After implementation, the maintainer verifies:

```text
$ scripts/validate.sh
ok: <… intermediate checks …>
ok: slides/beginner/part-01-meet-claude-code.md: deck sections (10/10)
ok: slides/beginner/part-01-meet-claude-code.md: duration marker = 20 min
… (one ok: per beginner check, per file) …
ok: beginner module duration sum = 210 (range 200..240)
ok: GLOSSARY.md: 0 orphan terms, 0 drift, all unique
ok: assessments/beginner/quiz.md: 16/16 questions, 2 per module
ok: skills/beginner (optional, none authored)
Result: N ok, 0 fail
```
