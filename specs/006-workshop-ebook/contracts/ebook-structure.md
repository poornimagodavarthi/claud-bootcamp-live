# Contract: Ebook Structure (reader-facing)

This contract defines the required structure and table of contents of the generated ebook. The validation gate (`scripts/check-ebook.sh`) verifies the output conforms to it.

## Top-level document order

```text
# Claude Code Bootcamp — Build 10 Real-World Projects with Claude Code   (H1, once)

## Front matter
  - Title page block (title, subtitle, instructor, edition)
  - How to use this book (intro; states whether solutions are included)
  - Prerequisites / pre-work
  - Table of contents (links to every chapter below)

## 01. Setup & AI-First Mindset
  ... prose ...
  ### Hands-on exercise — Module 01
  ### Solution — Module 01            (if include_solutions)

## 02. Prompting
  ... (same chapter shape) ...

## 03. … through … ## 10.   (each: prose → exercise → solution)

## 11. Q&A & Next Steps
  ... prose only (no exercise) ...

## Appendix A — Skills Library
  (from skills/README.md)
```

> **Branding:** the ebook is an unbranded edition. Packt branding and
> certification/exam framing are redacted from imported slide/exercise content
> during the build (the slide source files are left unchanged). There is no
> certification appendix.

## Structural assertions (MUST hold in the built output)

| ID | Assertion |
|----|-----------|
| ST-1 | Exactly one `#` (H1) line: the book title. |
| ST-2 | Chapters `## 01.` … `## 11.` appear in ascending numeric order. |
| ST-3 | A "Table of contents" section exists in front matter and links resolve to in-document anchors. |
| ST-4 | Each of chapters 01–10 contains a "Hands-on exercise" subsection. |
| ST-5 | If `include_solutions: true`, each of chapters 01–10 contains a "Solution" subsection. |
| ST-6 | Outside fenced code blocks, no line matches Marp frontmatter delimiters at file scope, `<!-- ... -->` directive/speaker-note comments, or `class=`/`marp:`/`paginate:` slide-chrome tokens. (Content inside ``` fences is exempt, so exercise snippets containing `---` or comments do not trip the gate.) |
| ST-7 | Every in-document link `[...](#anchor)` has a matching heading anchor (no broken internal links). |
| ST-8 | Front matter contains a title page and an introduction; back matter contains the skills overview appendix. |
| ST-9 | Content images render as standard Markdown `![]()` and fenced ```mermaid``` blocks are preserved; no raw decorative HTML slide chrome survives (FR-010). |
| ST-10 | No Packt branding or certification/exam framing survives outside fenced code blocks (the ebook is an unbranded edition; slide sources are unchanged). |
| ST-11 | The ebook is self-contained: no external relative file references survive; images are inlined as base64 data URIs so it renders detached from the repository. |

## Anchor naming

- Chapter anchors are chapter-scoped to avoid collisions on repeated subheadings (e.g., `#01-setup-ai-first-mindset`, `#01-hands-on-exercise`, `#02-hands-on-exercise`).
- TOC entries link to these scoped anchors only.

## Leanpub (Markua) manuscript variant

`scripts/build_leanpub.py` (wrapper `scripts/build-leanpub.sh`) renders the same content as a Leanpub-publishable Markua manuscript under `book/leanpub/manuscript/`, reusing the single-file transform/redaction pipeline. Differences from the single-file ebook:

- One file per chapter (Markua `#` = chapter; body headings shift down one level); `Book.txt` lists order, `Sample.txt` lists the free sample.
- `{frontmatter}` / `{mainmatter}` / `{backmatter}` section markers; no manual TOC (Leanpub generates it).
- Images are written to `resources/` and referenced as `resources/NAME.png`; SVG diagrams are rasterised to PNG at build time (data URIs are **not** used here). Intra-chapter cross-links use explicit `{#id}` heading attributes.

Validation gate `scripts/check-leanpub.sh`:

| ID | Assertion |
|----|-----------|
| LP-1 | Every file listed in `Book.txt` exists. |
| LP-2 | Each numbered chapter and the appendix has exactly one `#` chapter heading (fence-aware); front matter has at least one. |
| LP-3 | `{frontmatter}` + `{mainmatter}` markers in front matter; `{backmatter}` in the appendix. |
| LP-4 | Every `resources/…` image reference resolves to a real file. |
| LP-5 | Every intra-file `[...](#id)` link resolves to a `{#id}` in the same file. |
| LP-6 | No data URIs and no external `../` references survive. |
| LP-7 | No leaked Marp/HTML chrome and no Packt/certification/exam branding outside fenced code. |
