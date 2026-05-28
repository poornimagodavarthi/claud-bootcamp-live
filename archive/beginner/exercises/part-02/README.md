# Module 02 — Your first real conversation

> Run a 3-turn conversation with Claude Code and save the transcript.

## What you'll build

A file `~/three-turns.txt` containing three of your own prompts and the three replies Claude gave you, all inside the same Claude Code session.

## Before you start

- Module 01 is done; `~/first-prompt.txt` already exists.
- You can start `claude` and reach the `>` prompt.
- Pick a topic before you sit down. Anything you genuinely want to know: "How does HTTPS work?", "What is a closure in JavaScript?", "Why do I run out of disk space so often?".

## Step-by-step

1. Start Claude Code: `claude`.
2. **Turn 1**: ask your open question.
3. **Turn 2**: pick one follow-up and type it: `shorter`, `give me an example`, or `now explain it to a beginner`.
4. **Turn 3**: type `summarise that in one sentence`.
5. Copy the full back-and-forth — all three prompts and all three replies — into `~/three-turns.txt`. Save.
6. Type `/exit`.

Keep the conversation under 8 minutes. If a reply is missing or confusing, ask one more follow-up before saving, but stay inside the same session.

## The prompt to paste

There is no fixed prompt for this exercise. The literal text you'll re-use is the **second** turn. Pick exactly one of these and paste it verbatim:

```text
shorter
```

```text
give me an example
```

```text
now explain it to a beginner
```

## How to know it worked

Run these three checks:

```sh
test -s ~/three-turns.txt && echo "file has content"
grep -c '^>' ~/three-turns.txt
grep -c '.' ~/three-turns.txt
```

You should see:

```text
file has content
3
20+    (a number of total lines, usually 20–60)
```

(`grep -c '^>'` counts how many lines start with `>` — that should be 3, one per prompt. If you see 0, you probably stripped the `>` characters when you copied; that's fine, just add a `> ` prefix to each prompt line by hand.)

The [`solution/three-turns.example.txt`](solution/three-turns.example.txt) file in this folder shows what a passing transcript looks like — yours will differ in topic and wording.

## If something went wrong

| Symptom | Fix |
|---|---|
| Claude treats my Turn 2 as a brand-new question | You probably exited and reopened. Run the 3 turns in a single `claude` session. |
| My follow-up returned exactly the same answer | Try a stronger follow-up: `shorter — one sentence max` or `same idea, but as a single bullet list`. |
| The transcript file is empty | Your terminal may not be saving scrollback. Copy each reply by hand right after it appears, before you scroll. |
| I accidentally exited mid-conversation | Start over. The session memory does not persist across `/exit`. |

## You did it!

If `~/three-turns.txt` has three prompts and three replies from the same session, you've completed your first real Claude Code conversation. Continue to [Module 03 — Asking for what you want](../part-03/README.md).
