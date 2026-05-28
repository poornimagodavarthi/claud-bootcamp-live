# Claude Code 101 — Quiz Answer Key

One entry per question, in the form: `<N>. <Letter> — <source> — <rationale>.`

Source citations reference the slide module and an approximate slide name so you can re-read in context.

---

1. B — module-01 slide "Show me" — The deck shows `$ claude --version` returning `claude-code/1.4.2`; the convention is two dashes plus the word `version`.
2. C — module-01 slide "The one concept" / "Show me" — Inside the `claude` session prompts go after the `>` marker; the `$` is the regular shell, not Claude.
3. B — module-02 slide "The one concept" — Every prompt in the same session can see every previous prompt and reply; that is what makes follow-ups like "shorter" work.
4. C — module-02 slide "The one concept" — `/exit` ends the session; the next `claude` invocation starts fresh.
5. C — module-03 slide "The one concept" — A constraint is a hard limit such as a word count, jargon ban, or list of words to avoid.
6. C — module-03 slide "Show me" — Role + goal + constraint + format together produce the focused, actionable answer.
7. B — module-04 slide "Why this matters" — Reading does not change files, so nothing breaks if Claude is wrong; that is the lowest-stakes way to build trust.
8. C — module-04 slide "Common mistakes" — Pasting too much causes Claude to skim and miss the important parts; 30–80 lines at a time is the recommended ceiling.
9. B — module-05 slide "The one concept" — `git restore <file>` returns the file to the last committed state.
10. C — module-05 slide "The one concept" — Committing before edits is what makes every Claude edit reversible with a single `git restore`.
11. B — module-06 slide "The one concept" — CLAUDE.md lives at the repo root next to `.git`; that is where Claude looks on session start.
12. C — module-06 slide "The one concept" — The 20-line cap is for the author, not the tool: short files actually get updated, long ones go stale.
13. B — module-07 slide "The one concept" — A real password in a connection string is a secret; never paste it unredacted.
14. B — module-07 slide "Show me" — Replace the secret with `REDACTED` (or another obvious placeholder) before pasting; Claude can debug the shape without the real value.
15. C — module-08 slide "The one concept" / "Show me" — Each row is `<id><TAB><text>`; the grader compares stdout exactly.
16. B — module-08 slide "Show me" / "Common mistakes" — IDs are monotonic across the store; deleting id 1 does NOT free it for reuse, so the next add returns 2 (or higher).
