# Slide Decks — Claude Code Bootcamp

Marp-flavored Markdown sources for all 10 module decks. Build outputs go to `slides/dist/` (gitignored).

## Decks

| # | File | Module | Minutes |
|---|---|---|---:|
| 1 | [`part-01-setup-mindset.md`](part-01-setup-mindset.md) | Welcome, Setup & AI-First Mindset | 20 |
| 2 | [`part-02-prompting.md`](part-02-prompting.md) | Prompting Like a Tech Lead | 24 |
| 3 | [`part-03-claude-md.md`](part-03-claude-md.md) | Project Context with CLAUDE.md | 22 |
| 4 | [`part-04-best-of-n.md`](part-04-best-of-n.md) | Build Faster with Best-of-N | 30 |
| 5 | [`part-05-testing-debugging.md`](part-05-testing-debugging.md) | Testing, Debugging & Self-Review | 28 |
| 6 | [`part-06-git-workflows.md`](part-06-git-workflows.md) | Git Workflows for Safe AI Dev | 22 |
| 7 | [`part-07-multimodal.md`](part-07-multimodal.md) | Multimodal: Screenshot to UI | 30 |
| 8 | [`part-08-refactor-docs.md`](part-08-refactor-docs.md) | Refactoring & Documentation at Scale | 24 |
| 9 | [`part-09-skills-workflows.md`](part-09-skills-workflows.md) | Commands, Hooks & Reusable Workflows | 22 |
| 10 | [`part-10-production-readiness.md`](part-10-production-readiness.md) | Production Readiness | 18 |
| | | **Total instruction** | **240** |

## Required deck shape

Every deck satisfies the contract at [`../specs/001-bootcamp-course-materials/contracts/slide-deck.contract.md`](../specs/001-bootcamp-course-materials/contracts/slide-deck.contract.md):

- Marp frontmatter with `marp: true`, `theme`, `paginate: true`, `size: 16:9`, `title`, `description`
- A `<!-- duration: NN min -->` marker matching the table above
- 14 H2 sections in order: Title · Promise · Why this matters · Concepts · Live demo flow · Mini project · Step-by-step lab · Suggested Claude Code prompts · Deliverable checklist · Definition of done · Review checkpoint · Common mistakes · Instructor notes · Transition to next module

## Build

```bash
./deploy-pptx.sh              # PPTX only       → dist/pptx/
./deploy-pptx.sh --pdf        # PPTX + PDF      → dist/pdf/
./deploy-pptx.sh --html       # PPTX + HTML     → dist/html/
./deploy-pptx.sh --all        # PPTX + PDF + HTML
./deploy-pptx.sh --clean      # remove dist/ first
./deploy-pptx.sh --help
```

The script auto-detects a global `marp` binary and falls back to `npx --yes @marp-team/marp-cli@latest`. If Marp cannot locate Chromium for PPTX/PDF export, point it explicitly:

```bash
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
./deploy-pptx.sh --pdf
```

## Build outputs

```text
slides/dist/
├── pptx/    part-01-setup-mindset.pptx … part-10-production-readiness.pptx
├── pdf/     (when --pdf or --all)
└── html/    (when --html or --all)
```

`slides/dist/` is gitignored.
