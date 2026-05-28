# Claude Code 101 — Knowledge Quiz

16 multiple-choice questions, 2 per module. Pick exactly one answer per question. Passing threshold: **12/16**. Answer key is in [`answer-key.md`](answer-key.md) — try the quiz first before peeking.

Each question is preceded by an HTML comment that names the module the question comes from. Use it as a hint for which deck to re-read if you get stuck.

---

<!-- module: 01 -->

### Q1. After you finish Module 01, which command should print a version number in your terminal?

A. `claude version`
B. `claude --version`
C. `version claude`
D. `npm version claude-code`

<!-- module: 01 -->

### Q2. In a Claude Code session, where do you type your prompt?

A. At the regular shell prompt that starts with `$`.
B. Inside a separate browser window.
C. After the `>` prompt that appears once you run `claude`.
D. In a configuration file before you start the session.

<!-- module: 02 -->

### Q3. Inside a single `claude` session, why does the follow-up "shorter" work without repeating the original question?

A. Claude searches your shell history for the previous prompt.
B. Every prompt in the same session can see every previous prompt and reply.
C. The shell automatically prepends your last prompt to every new one.
D. "shorter" is a built-in keyword that re-runs the previous command.

<!-- module: 02 -->

### Q4. What ends a Claude Code conversation and starts the next one fresh?

A. Pressing Enter twice.
B. Typing `clear`.
C. Typing `/exit`.
D. Closing the terminal tab is the only way.

<!-- module: 03 -->

### Q5. In the role + goal + constraint + format prompt pattern, which piece is "no jargon, ≤ 50 words"?

A. Role.
B. Goal.
C. Constraint.
D. Format.

<!-- module: 03 -->

### Q6. Which prompt is most likely to return an actionable answer the first time?

A. `Make my code better.`
B. `Review this please.`
C. `Act as a careful Python reviewer. Find at most 3 real bugs, in order of severity. No style nits. Numbered list, each entry < 15 words.`
D. `Be concise and don't make any mistakes.`

<!-- module: 04 -->

### Q7. Why is reading code with Claude a low-stakes way to build trust?

A. Because Claude is always right about code it reads.
B. Because reading does not change files, so nothing breaks if Claude is wrong.
C. Because Claude automatically runs the code in a sandbox first.
D. Because Claude only reads code that has tests.

<!-- module: 04 -->

### Q8. When you paste 800 lines and ask "explain this", what is the most likely failure?

A. Claude refuses to answer.
B. Claude only explains the last 10 lines.
C. Claude skims and misses the important parts.
D. Claude prints the file back to you with no commentary.

<!-- module: 05 -->

### Q9. What single command returns a file to the last committed state?

A. `git revert <file>`
B. `git restore <file>`
C. `git undo <file>`
D. `git reset --hard <file>`

<!-- module: 05 -->

### Q10. Which habit makes every Claude edit reversible?

A. Saving the file to a backup folder before editing.
B. Telling Claude "do not change anything destructive".
C. Committing all current work in Git **before** asking Claude to edit.
D. Running every diff through a linter before accepting.

<!-- module: 06 -->

### Q11. Where does CLAUDE.md need to live for Claude to read it automatically?

A. In your home directory.
B. At the root of your project, next to `.git`.
C. In `~/.config/claude/`.
D. In any folder named `docs/`.

<!-- module: 06 -->

### Q12. Why does this beginner course recommend keeping CLAUDE.md under 20 lines?

A. Claude truncates anything longer.
B. Git refuses to commit files larger than 20 lines.
C. Short files actually get updated; long ones go stale.
D. Performance: every extra line slows the model down noticeably.

<!-- module: 07 -->

### Q13. Which of these should you NEVER paste into a Claude session unredacted?

A. A snippet of open-source code.
B. A connection string containing a real password.
C. An error message from a public stack trace.
D. The output of `claude --version`.

<!-- module: 07 -->

### Q14. You need help with a config file that contains one real API key. What is the safe move?

A. Paste it and ask Claude not to remember it.
B. Replace the API key with `REDACTED` (or a placeholder) before pasting.
C. Paste it but warn Claude that it is sensitive.
D. Email the file to yourself first as a backup, then paste.

<!-- module: 08 -->

### Q15. The capstone grader expects `python notes.py list` to print rows in what exact format?

A. `<id>, <text>` (comma-separated).
B. `<id> <text>` (single space).
C. `<id>\t<text>` (literal TAB between id and text).
D. `[<id>] <text>` (square brackets around id).

<!-- module: 08 -->

### Q16. After `python notes.py delete 1`, what should the next `python notes.py add "x"` print?

A. `added: 1` (reuses the freed id).
B. `added: 2` (or higher — ids are monotonic).
C. `added: 0` (counts from zero again).
D. Nothing — `add` is now disabled until you `list`.
