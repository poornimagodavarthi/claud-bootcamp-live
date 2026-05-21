# Module 06 — CLAUDE.md cheat sheet

> Write a 15-line CLAUDE.md and verify Claude actually uses it.

## What you'll build

A `CLAUDE.md` at the root of the starter project that answers five questions, plus proof that Claude reads it.

## Before you start

- Modules 01–05 are done.
- 12 minutes.

## Step-by-step

1. Copy the starter to a working location:
   ```sh
   cp -R exercises/beginner/part-06/starter ~/m6
   cd ~/m6
   ```
2. Open `CLAUDE.md` in your editor. It's currently a one-line placeholder.
3. Answer these five questions in the file, using the format from [`solution/CLAUDE.md`](solution/CLAUDE.md):
   - **What is this project, in one sentence?**
   - **Language & version?**
   - **How do I run it?**
   - **How do I test it?**
   - **What is the single most surprising convention?**
4. Keep the whole file under 20 lines.
5. Start `claude` from inside `~/m6`.
6. Ask the prompt below. Claude should answer using **your** CLAUDE.md, not generic advice.
7. Copy Claude's reply into `~/m6/claude-md-proof.txt`.

## The prompt to paste

```text
Without asking me any clarifying questions, tell me: what command runs the tests for this project, and what is the one convention I should not violate?
```

## How to know it worked

```sh
wc -l CLAUDE.md                           # → 5–20 lines
grep -c '^##' CLAUDE.md                   # → 2 or more H2 sections
grep -i 'pytest\|json\|one file' ~/m6/claude-md-proof.txt  # → at least 1 match
```

If Claude's reply names the literal test command and convention from **your** file (without you pasting CLAUDE.md into the chat), it read the file on its own. Compare with [`solution/CLAUDE.md`](solution/CLAUDE.md).

## If something went wrong

| Symptom | Fix |
|---|---|
| Claude asked "what's the test command?" | You probably started `claude` from the wrong directory. `cd ~/m6` and re-run. |
| Claude gave a generic answer about Python projects | Your CLAUDE.md may be empty or missing. `cat CLAUDE.md` to confirm. |
| The file is 60 lines long | Trim. Beginner CLAUDE.md should be ≤ 20 lines. Delete every line that is opinion, not fact. |
| Claude contradicts CLAUDE.md | The model is sometimes wrong. Re-prompt: `Re-read CLAUDE.md. The test command is what?`. |

## You did it!

If Claude can name your test command and your "do not violate" rule on the first try, your CLAUDE.md is doing its job. Continue to [Module 07 — Safer & smarter](../part-07/README.md).
