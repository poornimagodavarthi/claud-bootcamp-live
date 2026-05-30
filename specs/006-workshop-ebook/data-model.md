# Phase 1 Data Model: Workshop Markdown Ebook

This feature has no database. The "data model" is the logical document structure the build produces and the manifest that drives it.

## Entity: Ebook

The single consolidated Markdown output document.

| Field | Description | Source |
|-------|-------------|--------|
| `title` | Course title | `README.md` H1 / manifest |
| `subtitle` | Tagline | `README.md` blockquote / manifest |
| `instructor` | Instructor name | `README.md` / manifest |
| `edition` | Edition or date label | manifest (e.g., "May 2026") |
| `frontMatter` | Title page + introduction | generated + `README.md` |
| `chapters[]` | Ordered list of Chapter (parts 01–11) | manifest + `slides/` + `exercises/` |
| `backMatter` | Skills overview | `skills/README.md` |

**Validation rules**:
- `chapters` MUST contain exactly the 11 parts in ascending order (FR-001, SC-002).
- `frontMatter` MUST include a title page and an introduction (FR-002).
- A generated table of contents MUST link to every chapter (FR-003).

## Entity: Chapter

One workshop part rendered as prose.

| Field | Description | Source |
|-------|-------------|--------|
| `number` | 01–11 | manifest |
| `title` | Human-readable part title | slide frontmatter `title:` |
| `heading` | `## NN. Title` anchor (chapter-scoped) | derived |
| `body` | Prose-converted slide content | `slides/part-NN-*.md` |
| `exercise` | Embedded exercise brief (parts 01–10) | `exercises/part-NN/README.md` |
| `solution` | Reference solution appendix (parts 01–10) | `exercises/part-NN/solution/` |

> **Unbranded edition**: Chapter 11 ("Q&A & Next Steps") renders the part-11 deck as a normal chapter (recap, Q&A, next-steps narrative). The ebook ships without Packt branding or certification/exam framing: such references are redacted from imported slide/exercise content during the build (slide source files are left unchanged per Constitution Principle III). There is no certification appendix.

**Validation rules**:
- `body` MUST be free of Marp frontmatter, `<!-- ... -->` directives/speaker notes, slide separators, and HTML slide chrome (FR-004, SC-004).
- Parts 01–10 MUST have a non-empty `exercise` (FR-005, SC-003).
- Internal heading anchors MUST be unique within the Ebook (FR-008).

## Entity: Manifest (`scripts/ebook/manifest.json`)

Declarative configuration that drives the build. Keeps ordering/metadata out of code. Stored as JSON and parsed with the Python stdlib `json` module (no YAML dependency — Constitution Principle X).

```json
{
  "metadata": {
    "title": "Claude Code Bootcamp",
    "subtitle": "Build 10 Real-World Projects with Claude Code",
    "instructor": "Luca Berton",
    "edition": "May 2026",
    "include_solutions": true
  },
  "front_matter": { "source": "README.md" },
  "chapters": [
    { "number": "01", "slide": "slides/part-01-setup-mindset.md", "exercise": "exercises/part-01/README.md", "solution": "exercises/part-01/solution/" }
    // ... parts 02–10 ...
    , { "number": "11", "slide": "slides/part-11-qa-exam-next-steps.md", "exercise": null, "solution": null }
  ],
  "back_matter": {
    "skills": "skills/README.md"
  }
}
```

> Note: JSON has no comments; the `//` lines above are illustrative only and are not present in the real file. `include_solutions` is the FR-011 toggle. The build redacts Packt/certification/exam branding from imported content (see the unbranded-edition note above).

**Validation rules**:
- Every `slide` / `exercise` / `solution` path that is non-null MUST exist (build fails fast otherwise).
- `chapters` order is the authoritative reading order.

## Entity: Link Map (in-memory)

Built at runtime from the manifest: maps each included source file path → its in-document anchor. Used to rewrite relative cross-references (FR-007, SC-005). Targets not in the map are converted to absolute repo URLs or plain text.

## State / Lifecycle

The ebook is a pure derivation — no persistent state. Lifecycle is: **source files change → run `build-ebook.sh` → `check-ebook.sh` validates → gitignored output refreshed**. Regeneration is idempotent (FR-009, SC-006).
