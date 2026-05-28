# Contract — Build Output Layout

**Feature**: 004 Intermediate Course Content Polish
**Consumers**: `slides/deploy-pptx.sh`, `scripts/check-slide-overflow.sh`, downstream tooling that ships artefacts to learners or hosting.

This contract pins the directory layout under `slides/dist/` after FR-018 + Q1 (= A). It is the only contract that touches the build pipeline.

---

## Canonical layout

```text
slides/dist/                              # gitignored (Constitution Principle III)
├── intermediate/
│   ├── pptx/
│   │   ├── part-01-setup-mindset.pptx
│   │   ├── part-02-prompting.pptx
│   │   ├── part-03-claude-md.pptx
│   │   ├── part-04-best-of-n.pptx
│   │   ├── part-05-testing-debugging.pptx
│   │   ├── part-06-git-workflows.pptx
│   │   ├── part-07-multimodal.pptx
│   │   ├── part-08-refactor-docs.pptx
│   │   ├── part-09-skills-workflows.pptx
│   │   └── part-10-production-readiness.pptx
│   ├── pdf/
│   │   └── …same 10 basenames, .pdf extension
│   └── html/
│       └── …same 10 basenames, .html extension
└── beginner/
    ├── pptx/
    │   └── …8 beginner deck basenames, .pptx
    ├── pdf/
    │   └── …8 beginner deck basenames, .pdf
    └── html/
        └── …8 beginner deck basenames, .html
```

**Total artefacts on a full clean build**: `(10 intermediate + 8 beginner) × 3 formats = 54`.

---

## Audience-derivation rule

`slides/deploy-pptx.sh` MUST derive the `audience` segment from the source deck path:

| Source path glob | `audience` value |
|---|---|
| `slides/beginner/part-*.md` | `beginner` |
| `slides/part-*.md` | `intermediate` |

No other source paths are valid inputs. If a future audience is added (e.g., advanced), it MUST be added via a third top-level subdirectory; mixing audiences in one subtree is forbidden.

---

## Path-construction contract

For each source deck `<src>` and each format `<fmt> ∈ {pptx, pdf, html}`:

```text
output_path = slides/dist/<audience(src)>/<fmt>/<basename(src, .md)>.<fmt>
```

`deploy-pptx.sh` MUST pass this exact path as Marp's `--output` flag. Marp MUST NOT be invoked with a directory-only `--output` (which would let Marp pick the basename and break the contract).

The script MUST `mkdir -p` the output directory before invoking Marp; missing directories MUST NOT cause Marp to bail.

---

## Backward-compatibility break

The previous flat layout (`slides/dist/{pptx,pdf,html}/<basename>.<fmt>`) is **removed**. Any downstream consumer (hosting pipeline, packaging script, `.gitignore`, README documentation) that referenced the flat layout MUST be updated.

**Required follow-up edits inside this feature**:

- `slides/README.md` — update the "Where the build artefacts land" paragraph (if present).
- `.gitignore` — confirm `slides/dist/` (without a trailing format-specific subdir) is the entry, so the new subtrees are covered automatically.
- `instructor-guide.md` / `student-guide.md` — only if they reference build paths (audit grep; expected empty).

**Required follow-up edits outside this feature**: none — exercises/skills/assessments do not reference `slides/dist/`.

---

## Hand-off scenarios this layout enables

Three concrete scenarios named in the spec:

1. **"Send me the intermediate PDFs."** → `cp -r slides/dist/intermediate/pdf/ /tmp/handoff/`
2. **"Ship just Day-1 morning content."** → `cp -r slides/dist/intermediate/{pptx,pdf}/ /tmp/handoff/` (intermediate = Day 1 morning per Module-numbering convention).
3. **"Quickly preview every deck in a browser."** → `python3 -m http.server 8080 -d slides/dist/` then browse to `/intermediate/html/` or `/beginner/html/`.

---

## Verification

After `rm -rf slides/dist && ./slides/deploy-pptx.sh --all`:

```bash
# Expect exactly 6 leaf directories
find slides/dist -mindepth 2 -maxdepth 2 -type d | sort
# Expected output:
#   slides/dist/beginner/html
#   slides/dist/beginner/pdf
#   slides/dist/beginner/pptx
#   slides/dist/intermediate/html
#   slides/dist/intermediate/pdf
#   slides/dist/intermediate/pptx

# Expect exactly 54 leaf files
find slides/dist -type f | wc -l
# Expected: 54

# Expect 10 files in each intermediate format directory
ls slides/dist/intermediate/pptx | wc -l   # 10
ls slides/dist/intermediate/pdf  | wc -l   # 10
ls slides/dist/intermediate/html | wc -l   # 10

# Expect 8 files in each beginner format directory
ls slides/dist/beginner/pptx | wc -l       # 8
ls slides/dist/beginner/pdf  | wc -l       # 8
ls slides/dist/beginner/html | wc -l       # 8

# Expect no stray files at slides/dist/ root or at slides/dist/<audience>/ root
find slides/dist -maxdepth 1 -type f       # empty
find slides/dist -maxdepth 2 -type f       # empty
```

All five assertions MUST pass. They are part of SC-003 + SC-006 verification.
