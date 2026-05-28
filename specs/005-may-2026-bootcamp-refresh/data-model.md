# Data Model — May 2026 Bootcamp Refresh

**Feature**: 005-may-2026-bootcamp-refresh
**Date**: 2026-05-28

This feature ships content, not running code. The "data model" is the set of repository entities the audit script reads and the published artefacts students consume. Each entity below carries a stable identity, fields, validation rules, and the audit gate that enforces it.

---

## 1. `Module` (Agenda Part)

**Identity**: `module_number` (01–10) + `slug` (kebab).

| Field | Type | Source | Validation |
|---|---|---|---|
| `module_number` | `int` 01–10 | folder name | unique; sequential; no gaps |
| `slug` | string (kebab) | folder name | matches `^[a-z][a-z0-9-]+$` |
| `title` | string | `slides/part-NN-*.md` frontmatter `title:` | non-empty; matches `README` agenda row |
| `duration_min` | int | `<!-- duration: NN min -->` in deck | sum across 01–10 = 240 ± 5 (Constitution Authoring) |
| `deck_path` | path | derived | exists; readable |
| `exercise_path` | path | derived | exists; has `README.md` |
| `solution_path` | path | derived | exists; has runnable entry point |

**Audit gate**: `audit.module-bundle` — for each NN 01–10 verifies deck + exercise + solution all present and cross-linked.

---

## 2. `SlideDeck`

**Identity**: `module_number` (or `11` for Q&A closing block).

| Field | Type | Source | Validation |
|---|---|---|---|
| `theme` | string | frontmatter `theme:` | == `wow-beginner` |
| `paginate` | bool | frontmatter | `true` |
| `size` | string | frontmatter | `16:9` |
| `sections[]` | string[] | H2 headings | superset of the 14 canonical sections (Constitution II): Title · Promise · Why this matters · Concepts · Live demo flow · Mini project · Step-by-step lab · Suggested Claude Code prompts · Deliverable checklist · Definition of done · Review checkpoint · Common mistakes · Instructor notes · Transition |
| `cut_line` | string | instructor-notes section | non-empty (FR-017) |
| `polish_log` | block | EOF HTML comment | block present (FR-020) |
| `inline_svgs[]` | path[] | `![h:NNN](intermediate/assets/*.svg)` | each exists; each constrained by `h:` ≤ 320 |

**State transitions**: `draft` (in spec) → `built` (PDF/PPTX/HTML in `slides/dist/`) → `published` (committed). The audit treats only `built` + `published` as in-scope.

**Audit gates**:
- `audit.slide-anatomy` — every required section heading present.
- `audit.slide-theme` — frontmatter `theme: wow-beginner`.
- `audit.slide-overflow` — passes `scripts/check-slide-overflow.sh --budget 22`.
- `audit.duration-sum` — Σ `duration_min` (01–10) == 240 ± 5.

---

## 3. `Exercise`

**Identity**: `module_number`.

| Field | Type | Source | Validation |
|---|---|---|---|
| `sections[]` | string[] | H2 headings in `README.md` | superset of the 9 canonical (Constitution II): Goal · Scenario · Starter instructions · Claude Code prompt to use · Manual validation steps · Expected deliverable · Definition of done · Stretch challenge · Troubleshooting |
| `prerequisites` | list | "Goal" / "Scenario" header | non-empty |
| `expected_duration_min` | int | front-matter or header | ≤ matching `SlideDeck.duration_min` |
| `acceptance_criteria` | list | "Definition of done" | ≥ 3 testable items |
| `solution_link` | path | inline link | resolves to `solution/` |

**Audit gate**: `audit.exercise-anatomy`.

---

## 4. `ReferenceSolution`

**Identity**: `module_number`.

| Field | Type | Source | Validation |
|---|---|---|---|
| `entry_point` | path | `solution/README.md` or `solution/run.sh` | exists; executable when shell script |
| `stack` | enum | declared in solution README | one of `python3.11`, `node20`, `shell`, `markdown-only` |
| `expected_runtime_s` | int | declared | ≤ 300 (SC-007: 5 min) |
| `deliverable_matches_rubric` | bool | manual review | every rubric item green |

**Audit gate**: `audit.solution-presence` (existence + entry point); runtime is human-verified in the dress rehearsal (SC-009).

---

## 5. `Skill`

**Identity**: `slug` under `skills/`.

| Field | Type | Source | Validation |
|---|---|---|---|
| `name` | string | SKILL.md frontmatter | matches folder name |
| `description` | string | SKILL.md frontmatter | non-empty |
| `body_sections[]` | string[] | H2 in body | exactly 6: Purpose · When to use · Body · Inputs · Outputs · Worked example |
| `project_agnostic` | bool | text scan | no occurrences of `module-NN/`, `exercises/part-NN/`, `slides/part-NN-*` paths |

**Catalogue** (FR-011 + FR-012 + FR-013): 12 skills total. Existing 10 + new `release-readiness` + new `mcp-context-brief`.

**Audit gate**: `audit.skill-contract` (delegates to existing `specs/001-bootcamp-course-materials/contracts/skill.contract.md`).

---

## 6. `AssessmentItem`

**Identity**: question/task ID inside `assessments/`.

| Field | Type | Source | Validation |
|---|---|---|---|
| `kind` | enum | filename | one of `knowledge-quiz`, `practical-task`, `code-review-reflection`, `rubric`, `answer-key` |
| `module_ref` | int 01–10 | item body | maps to ≥1 published module |
| `weight_pct` | int | rubric.md | conforms to 40% / 40% / 20% (Constitution VIII) |
| `pass_threshold_pct` | int | rubric.md | 70 (Constitution VIII) |
| `may2026_coverage` | enum | text scan | ≥1 item covers each of: Skills, MCP, Hooks, GitHub Actions, Multi-agent |

**Audit gate**: `audit.assessment-coverage`.

---

## 7. `AuditGate`

**Identity**: gate name (`audit.<slug>`).

| Field | Type | Description |
|---|---|---|
| `name` | string | e.g., `audit.cross-links` |
| `runs[]` | command | one or more shell commands |
| `pass_rc` | int | 0 |
| `fail_message` | string | template printed on RC≠0 with file:line pointer |
| `severity` | enum | `block` (fails preflight) or `warn` (prints, RC=0) |

**Master list**:

| Gate | Severity | Source |
|---|---|---|
| `audit.module-bundle` | block | new |
| `audit.slide-anatomy` | block | new |
| `audit.slide-theme` | block | existing (`check-verbatim-blocks.sh`) |
| `audit.slide-overflow` | block | existing (`check-slide-overflow.sh`) |
| `audit.duration-sum` | block | existing, threshold tightened to ±5 |
| `audit.exercise-anatomy` | block | new |
| `audit.solution-presence` | block | new |
| `audit.skill-contract` | block | new (wraps existing contract) |
| `audit.assessment-coverage` | block | new |
| `audit.cross-links` | block | new (intra-repo only — R-003) |
| `audit.bundle-coverage` | block | new (each May-2026 upgrade ≥1× in deck + exercise) |
| `audit.no-clarifications-in-published` | block | new |
| `audit.archive-isolation` | block | new (no primary nav link enters `archive/`) |
| `audit.dist-freshness` | warn | new (R-006) |
| `audit.contrast` | block | existing (`check-contrast.sh`) |

---

## 8. `PolishLogEntry`

**Identity**: `(module_number, date)`.

| Field | Type | Validation |
|---|---|---|
| `date` | YYYY-MM-DD | parseable |
| `cohort` | string | non-empty |
| `note` | text | one of: prompt-shape drift · timing tweak · student feedback |

**Use**: dated cohort tweaks recorded in the EOF HTML comment block of each deck (FR-020). Not validated by audit beyond presence of the surrounding marker.

---

## 9. `ArchiveItem` (off-agenda content)

**Identity**: source path under `archive/`.

| Field | Type | Validation |
|---|---|---|
| `original_path` | path | recorded at move time |
| `kind` | enum | `slide` / `exercise` / `assessment` / `guide` |
| `reason` | string | constant: `"Off-agenda — optional pre-bootcamp warm-up"` |
| `reachable_from_primary_nav` | bool | MUST be `false` (audit gate `audit.archive-isolation`) |

---

## Relationships

```text
README (1) ──linkset──> Module (10)
Module ── 1:1 ──> SlideDeck
Module ── 1:1 ──> Exercise ── 1:1 ──> ReferenceSolution
Module ── *:* ──> Skill          (via slide "Suggested prompts" + exercise "Claude Code prompt")
Module ── *:* ──> AssessmentItem (via rubric module_ref)
README ──linkset──> archive/ (labelled, single heading, no in-bootcamp link)
AuditGate ── operates on ──> {SlideDeck, Exercise, ReferenceSolution, Skill, AssessmentItem, ArchiveItem}
```

---

## Counts (target end-state)

| Entity | Count |
|---|---|
| Module (01–10) | 10 |
| SlideDeck (incl. Part 11 closing) | 11 |
| Exercise | 10 |
| ReferenceSolution | 10 |
| Skill | 12 (10 existing + 2 new) |
| AssessmentItem files | 5 (quiz, task, reflection, rubric, answer-key) |
| AuditGate | 15 |
| `slides/dist/` artefact | 33 (11 × 3 formats) |
