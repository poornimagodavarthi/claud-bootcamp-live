# Contract — Glossary Character-Identity Rule

**Feature**: `002-claude-beginner-course`  
**Applies to**: `GLOSSARY.md` and every deck's `## Glossary card` slide  
**Enforced by**: `scripts/validate.sh` (extension R3.8)  
**Spec**: FR-015, SC-006

---

## Rule

For every term that appears on any beginner deck's `## Glossary card` slide, an entry with the **identical term spelling and byte-identical definition** MUST exist in `GLOSSARY.md`. Conversely, every entry in `GLOSSARY.md` MUST be referenced by at least one beginner deck's Glossary card.

## Canonical line format

Both surfaces use the same one-line format:

```text
- **<Term>**: <One-line definition, ending with a period.>
```

Constraints:

- Exactly one leading `- ` (Markdown bullet).
- Term wrapped in `**…**`, followed by `: ` (colon + single space).
- Definition is exactly one line (no embedded newlines), ends with a period.
- Trailing whitespace is stripped before comparison.

## GLOSSARY.md structure

`GLOSSARY.md` MUST be a single Markdown file at repo root with the structure:

```markdown
# Glossary

> Plain-language definitions used throughout the Claude Code 101 beginner course.
> Every term here is introduced in at least one module's slide deck.

## A

- **Accept (a diff)**: Telling Claude Code "yes, apply this change to my file."
- **Analogy**: …

## C

- **Claude Code**: The official Anthropic command-line tool that brings Claude into your terminal.
- **CLI**: A program you control by typing commands instead of clicking.
- **CLAUDE.md**: …

## …
```

Entries are grouped under H2 letter headings (`## A`, `## C`, …) for human navigability. The validator ignores grouping headings and treats only `- **term**: definition` lines as data.

## Extraction algorithm (validator)

```text
1. From every slides/beginner/part-*.md:
     between the line matching '^## Glossary card$' and the next '^---$' or EOF,
     extract all lines matching '^- \*\*(.+?)\*\*: (.+)$' → (term, definition) pairs.
2. From GLOSSARY.md:
     extract all lines matching '^- \*\*(.+?)\*\*: (.+)$' → (term, definition) pairs.
3. For each deck entry (term, def_deck):
     find (term, def_glossary) in GLOSSARY.md;
     if missing → fail: "term '<term>' from <deck>:<line> not found in GLOSSARY.md"
     if def_deck != def_glossary → fail: "glossary drift for '<term>': deck says '<def_deck>', GLOSSARY.md says '<def_glossary>'"
4. For each glossary entry (term, _):
     if term not present in any deck → fail: "orphan glossary entry '<term>' in GLOSSARY.md:<line>"
5. Assert all terms in GLOSSARY.md are globally unique.
```

## Worked example

`slides/beginner/part-01-meet-claude-code.md`:

```markdown
## Glossary card

- **Claude Code**: The official Anthropic command-line tool that brings Claude into your terminal.
- **CLI**: A program you control by typing commands instead of clicking.
```

`GLOSSARY.md`:

```markdown
## C

- **Claude Code**: The official Anthropic command-line tool that brings Claude into your terminal.
- **CLI**: A program you control by typing commands instead of clicking.
```

Result: PASS for these two terms.

If the deck instead said:

```markdown
- **CLI**: A program you control by typing commands.
```

Result: FAIL with `glossary drift for 'CLI': deck says 'A program you control by typing commands.', GLOSSARY.md says 'A program you control by typing commands instead of clicking.'`

## Operational consequence for authors

The glossary is the single source of truth. Authors edit `GLOSSARY.md` first, then copy the canonical line into the deck's Glossary card. Never the other way around.
