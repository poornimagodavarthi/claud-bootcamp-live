# Quickstart — May 2026 Bootcamp Refresh

**Feature**: 005-may-2026-bootcamp-refresh
**Audience**: instructor / repo maintainer (the implementer of this feature).
**Date**: 2026-05-28

## In 5 minutes

```bash
# 1. Branch is already on 005-may-2026-bootcamp-refresh (created by the speckit hook)
git switch 005-may-2026-bootcamp-refresh
git status -sb   # should be clean

# 2. Build current state of all slides
( cd slides && ./deploy-pptx.sh --all )
ls slides/dist/pdf/ | wc -l   # 10 today; will become 11 after Part 11 lands

# 3. Run the existing audits (these will still PASS — they are the floor)
scripts/check-verbatim-blocks.sh && echo OK
scripts/check-slide-overflow.sh --budget 22 slides/dist/html && echo OK
scripts/check-contrast.sh && echo OK
```

## What this feature adds (in dependency order)

| Step | Output | Validates |
|---|---|---|
| 1 | `archive/beginner/` move | R-001 / FR-015 / `audit.archive-isolation` |
| 2 | `slides/part-11-qa-exam-next-steps.md` | R-002 / FR-009 / `audit.module-bundle` |
| 3 | `exercises/part-NN/{README,solution/}` for NN where missing | FR-002 / FR-005 / `audit.module-bundle` + `audit.exercise-anatomy` + `audit.solution-presence` |
| 4 | May-2026 content additions inside slides + exercises (per FR-004) | `audit.bundle-coverage` |
| 5 | New skills: `skills/release-readiness/SKILL.md`, `skills/mcp-context-brief/SKILL.md` | FR-012 / FR-013 / `audit.skill-contract` |
| 6 | Assessment updates for May-2026 coverage | FR-010 / `audit.assessment-coverage` |
| 7 | `scripts/preflight.sh` composing all gates | FR-016 / contract |
| 8 | Slide rebuild + dist refresh (33 artefacts) | SC-003 |

## Verify the end state

```bash
# 1. Pre-flight is green
scripts/preflight.sh
echo "RC=$?"     # must be 0

# 2. Slides build clean
( cd slides && time ./deploy-pptx.sh --all )
ls slides/dist/pdf/ | wc -l   # 11
ls slides/dist/pptx/ | wc -l  # 11
ls slides/dist/html/ | wc -l  # 11

# 3. Manual P1 stopwatch test
#    Hand the repo to a colleague who has not seen it.
#    They MUST reach exercises/part-01/README.md from README.md in < 60 s.

# 4. Dress rehearsal
#    Walk every slide deck. Run every demo prompt. Time it.
#    Σ duration_min(parts 01–10) == 240 ± 5.
```

## Roll back

```bash
# Everything in this feature is reversible via git.
git switch main
git branch -D 005-may-2026-bootcamp-refresh  # discard
# OR keep the branch and revert specific files:
git checkout main -- slides/part-09-skills-workflows.md
```

## Known issues / open follow-ups

- **R-006**: `slides/dist/` remains tracked (Constitution III divergence). Feature 006 candidate.
- **Anthropic interface drift**: polish-log dated notes are the only mitigation; no automated check.
- **Reference-solution runtime**: not audited automatically (LLM nondeterminism). Dress rehearsal only.
