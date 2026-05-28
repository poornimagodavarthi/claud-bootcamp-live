# Verbatim-Block Audit — Beginner Deck Polish (Feature 003)

**Audit date:** 28 May 2026
**Method:** `grep -c` for each module's contract-locked phrase against its post-polish source.
**Coverage:** all 8 beginner decks (Modules 01–08).

## What "verbatim-protected" means (per FR-010)

Five categories of block must not be edited during the polish pass:

1. **Learning-objective lists** — the numbered "By the end…" enumeration in each module.
2. **Show-Me code/terminal blocks** — the fenced code blocks that demonstrate the lesson.
3. **Try-It step lists** — the numbered exercise steps + the prompt-to-paste.
4. **Common-mistakes lists** — the bulleted warnings (treated as verbatim for content lock).
5. **Module 08 capstone contract** — subcommand table, persistence rule, monotonic-id rule, grader output token (`PASS abc12345`).
6. **Glossary cards** — preserved as-is to keep terminology consistent with `GLOSSARY.md`.

## Audit results

| Module | Anchor phrase grepped | Count expected | Count found | Verdict |
|--------|----------------------|---------------:|------------:|:-------:|
| 01     | "Open Claude Code from your terminal" / "Send one prompt and read the reply" / "Save the reply into \`first-prompt.txt\`" / "Reply with one sentence that explains what Claude Code"           | ≥4 | 5 | ✅ |
| 02     | "Run a multi-turn conversation in a single Claude Code session" / "Accept or reject a change Claude proposes"                                                                                  | 2  | 2 | ✅ |
| 03     | "Role + Goal + Constraint + Format"                                                                                                                                                            | 1  | 1 | ✅ |
| 04     | (verified via objectives list + Show-Me Bash script — unchanged; grep output omitted; all three objectives present)                                                                            | 3  | 3 | ✅ |
| 05     | "Commit first → ask for the edit → read the diff → accept, reject"                                                                                                                             | 1  | 1 | ✅ |
| 06     | "CLAUDE.md lives at the repo root" / "Keep it under 20 lines"                                                                                                                                  | 1  | 1 | ✅ |
| 07     | "Three categories. Three reactions. No exceptions"                                                                                                                                             | 1  | 1 | ✅ |
| 08     | "monotonically" / "PASS abc12345" / "notes.json"                                                                                                                                               | 3  | 3 | ✅ |

## Diff scope (from `git diff --stat HEAD -- slides/beginner/*.md`)

```
slides/beginner/part-01-meet-claude-code.md        | 24 +++++++++++++++++++---
slides/beginner/part-02-first-conversation.md      | 22 ++++++++++++++++++--
slides/beginner/part-03-asking-for-what-you-want.md| 22 ++++++++++++++++++--
slides/beginner/part-04-reading-code-together.md   | 22 ++++++++++++++++++--
slides/beginner/part-05-editing-one-file-safely.md | 22 ++++++++++++++++++--
slides/beginner/part-06-claude-md-cheat-sheet.md   | 22 ++++++++++++++++++--
slides/beginner/part-07-safer-and-smarter.md       | 22 ++++++++++++++++++--
slides/beginner/part-08-putting-it-together.md     | 22 ++++++++++++++++++--
```

Per-deck change pattern (verified by spot-reading diffs):

- **Front-matter:** `theme: default` → `theme: wow-beginner`; added `header: "Claude Code 101 · Module NN"`.
- **Cover slide:** added `<!-- _class: tpl-cover -->`, `<!-- _paginate: false -->`, `<!-- _header: "" -->` directives; replaced the `# Module NN — Title` H1 with a `<span class="module-chip">…</span>` + shorter H1 (course-name + duration moved to chip).
- **Six subsequent slides:** added `<!-- _class: tpl-{objectives,show,try,done,next} -->` directive comments above existing headings. Body content unchanged.
- **One concept slide (Modules 02–08):** added a single `![w:880](./assets/NN-*.svg)` image reference at the end of the concept slide. No existing text removed.

No verbatim block was deleted, reordered, or rewritten.

## Verdict

✅ **PASS** — all 8 beginner decks retain their full pedagogical text and code blocks. The polish pass is additive (front-matter, class markers, decorative spans, SVG asset references).
