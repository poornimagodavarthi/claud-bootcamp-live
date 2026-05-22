# Exercise Contract

**Audience**: authors of `exercises/part-NN/`; reviewers; `scripts/validate.sh`.
**Source rules**: Constitution Principles II, IV, VI; spec FR-012, FR-013, FR-014, FR-015, FR-015a, FR-015b.

An "exercise" is the lab packet for one module. There are exactly 10
exercises, one per module, each living in its own numbered directory.

## Directory layout

```
exercises/
└── part-NN/
    ├── README.md                   # the exercise itself; required for all 10
    ├── solution/                   # required for code-producing modules only
    │   ├── python/                 # required for modules 2, 4, 5, 7, 8 (Python primary)
    │   └── node/                   # required for modules 2, 4, 5 only (Node secondary)
    ├── code-review-rubric.md       # module 5 ONLY (renamed deliverable, FR-011)
    ├── wireframe.png               # module 7 ONLY (FR-015b)
    └── wireframe-sketch.png        # module 7 ONLY (FR-015b)
```

Conceptual modules (1, 3, 6, 9, 10) ship `README.md` only — no
`solution/` directory.

Code-producing modules ship a `solution/` directory:

| Module | Tracks under `solution/` |
|---|---|
| 2 (CLI Task Manager) | `python/` AND `node/` |
| 4 (Notes App API) | `python/` AND `node/` |
| 5 (Tests + Bug Fixes + Code Review Rubric) | `python/` AND `node/` |
| 7 (Dashboard UI) | `python/` only |
| 8 (Refactor + Handoff Docs) | `python/` only |

Each track directory MUST contain at least one runnable file (e.g.,
`main.py` / `package.json`+`src/main.ts`) plus a `README.md`
documenting how the instructor runs it.

## `exercises/part-NN/README.md` — required structure

The file MUST start with a level-1 heading and a "do not open
solution" notice (only when a `solution/` directory exists):

```markdown
# Exercise N — <Project Name>

> **For students**: do not open the `solution/` directory until you
> have completed your own attempt and run the Manual validation steps.
> Reference solutions are provided for grading and self-comparison
> only.

<!-- duration: NN min -->
<!-- module: N -->
<!-- project: <FR-011 canonical project name> -->
```

The 9 required H2 sections follow, in this exact order:

| # | Heading | Notes |
|---|---|---|
| 1 | `## Goal` | one paragraph, learner-facing |
| 2 | `## Scenario` | concrete narrative; ties the lab to a realistic situation |
| 3 | `## Starter instructions` | numbered prerequisites and setup steps; assumes pre-work is complete |
| 4 | `## Claude Code prompt to use` | a single fenced ```` ```text ```` block containing a complete copy-paste big prompt (FR-013) |
| 5 | `## Manual validation steps` | numbered, deterministic; each step has an observable command or behavior (FR-014) |
| 6 | `## Expected deliverable` | filenames and observable artifacts; matches Module's `expected_outputs` |
| 7 | `## Definition of done` | bulleted pass/fail self-checklist (Principle VI) |
| 8 | `## Stretch challenge` | one optional extension for fast finishers |
| 9 | `## Troubleshooting` | ≥ 3 (issue, fix) pairs, formatted as a table or definition list |

`scripts/validate.sh` checks for **presence in order** of these 9
headings.

## Section content rules

### `## Claude Code prompt to use` (section 4)

- MUST be inside a fenced ```` ```text ```` block.
- MUST be a complete big prompt: contains role/context, task,
  constraints, acceptance criteria, output format. No placeholders the
  student must fill.
- For modules with both Python and Node tracks (2, 4, 5), the file
  MUST contain TWO labeled prompt blocks (`### Python track` and
  `### Node.js track` H3 headings) before the fenced blocks.

### `## Manual validation steps` (section 5)

- Steps MUST be deterministic. Acceptable forms:
  - Shell commands with expected output (e.g., `pytest -q` →
    `=== 12 passed in 0.42s ===`).
  - File-existence checks (e.g., `[ -f api/main.py ]`).
  - Observable HTTP behavior (e.g., `curl http://localhost:8000/health`
    returns `{"status": "ok"}`).
- For modules with both tracks, validation steps SHOULD be
  parameterized (one numbered list with track-specific commands).

### `## Definition of done` (section 7)

- Bulleted pass/fail format. Bullets MUST start with a verifiable
  predicate ("Tests pass with no failures", "API returns 200 on
  /notes", etc.). No subjective phrasing.

### `## Troubleshooting` (section 9)

Definition list or two-column table:

```markdown
**Symptom**: `claude: command not found`
**Fix**: Ensure pre-work step 3 was completed; run `which claude` from
your shell.
```

## Module-specific rules

### Module 5

- File `exercises/part-05/code-review-rubric.md` MUST exist.
- It is the student-built deliverable, distinct from
  `assessments/rubric.md` (FR-011).
- The exercise's section 6 (Expected deliverable) MUST list it
  explicitly with the exact filename.

### Module 7

- Files `exercises/part-07/wireframe.png` (or `.svg`) AND
  `exercises/part-07/wireframe-sketch.png` (or `.svg`) MUST exist.
- The Claude Code prompt block (section 4) MUST reference
  `wireframe.png` by relative path.
- The reference solution (`solution/`) MUST implement the canonical
  wireframe so the rubric is deterministic.

## Build & run (reference solutions)

Each `solution/<track>/README.md` MUST document a single command to
run the solution and a single command to validate it. Example
(`solution/python/`):

```markdown
# Run

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python -m app

# Validate

    pytest -q
```

## Acceptance test (manual, per exercise)

1. `README.md` opens and starts with the H1 + notice + duration/module/project comments.
2. All 9 required sections present in order.
3. The Claude Code prompt block is a single fenced `text` block (or two
   labeled blocks for dual-track modules).
4. Manual validation steps are deterministic.
5. Definition of done is bulleted pass/fail.
6. Troubleshooting has ≥ 3 entries.
7. For code-producing modules: `solution/<track>/` runs and validates
   per its own README.
