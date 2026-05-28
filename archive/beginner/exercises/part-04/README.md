# Module 04 — Reading code together

> Ask Claude to explain an unfamiliar script line by line, then ask one follow-up.

## What you'll build

A file `~/code-read.txt` containing:

1. The script you handed to Claude (from [`starter/log_summary.sh`](starter/log_summary.sh) or your own).
2. Claude's plain-English explanation.
3. One follow-up question you asked, and Claude's reply.

## Before you start

- Modules 01–03 are done.
- You have a short script (5–30 lines). Use the sample if you don't have one.
- 10 minutes.

## Step-by-step

1. Open [`starter/log_summary.sh`](starter/log_summary.sh). Read it once on your own — it's fine if some lines are confusing; that's the point.
2. Start `claude`.
3. Paste this prompt followed by the script content:
   ```text
   Explain this script for someone who has never used Bash. Three short paragraphs.
   ```
4. Copy Claude's reply into `~/code-read.txt` under a `## Explanation` header.
5. Pick one line you still don't understand. Ask Claude about it specifically. Example: `What does set -euo pipefail catch?`.
6. Copy that exchange into `~/code-read.txt` under a `## Follow-up` header.
7. `/exit`.

## The prompt to paste

For step 3, this is the literal prompt:

```text
Explain this script for someone who has never used Bash. Three short paragraphs.
```

For step 5, the follow-up is your choice — anything that names a specific line or symbol.

## How to know it worked

```sh
grep -c '^##' ~/code-read.txt        # → 3 (script header, explanation, follow-up)
grep -c '^#!/usr/bin/env bash' ~/code-read.txt  # → 1 (script was pasted)
wc -l ~/code-read.txt                # → 30+ lines total
```

A reference transcript is at [`solution/code-read.example.txt`](solution/code-read.example.txt).

## If something went wrong

| Symptom | Fix |
|---|---|
| Claude says "I cannot see any code" | You forgot to paste the script after the prompt. Re-send with the script underneath. |
| The explanation is one giant paragraph | Add `Three short paragraphs.` to the prompt. The model needs the format hint. |
| The follow-up reply is unrelated | Quote the line literally. Example: `On the line that says \`set -euo pipefail\`, what does each flag do?` |
| I accidentally pasted too much (a whole project) | Trim down to one file at a time. Reading scales badly past ~100 lines. |

## You did it!

If your `~/code-read.txt` has the script, an explanation, and a follow-up — all under H2 headers — you've completed your first code-reading session with Claude. Continue to [Module 05 — Editing one file safely](../part-05/README.md).
