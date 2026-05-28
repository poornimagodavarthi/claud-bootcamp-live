# Module 01 — Meet Claude Code

> Send your first prompt to Claude Code and save the reply.

## What you'll build

A file at `~/first-prompt.txt` (in your home directory) that contains:

1. The exact prompt you sent to Claude.
2. The exact reply you got back.

Module 00 already walked you through this once. This exercise is the same flow, on its own, so you can repeat it without re-reading the setup steps.

## Before you start

- Module 00 is done: `claude --version` prints a version number on your machine.
- You are at a fresh terminal prompt (not already inside `claude`).
- You can write a file in your home directory (i.e. `echo hello > ~/test.txt` works).

If any of those three is not true, finish Module 00 first.

## Step-by-step

1. Open your terminal and confirm you are in your home directory: `cd ~ && pwd`. The output should be something like `/Users/yourname` (macOS) or `/home/yourname` (Linux).
2. Start Claude Code: `claude`.
3. At the `>` prompt, paste the prompt from the next section verbatim and press Enter.
4. Wait for the reply (usually 2–4 seconds).
5. Open a new file in your editor (or use `nano ~/first-prompt.txt`) and write two clearly-labelled sections: one for the prompt, one for the reply. Paste each verbatim.
6. Save the file. Type `/exit` in your `claude` session to leave it.

## The prompt to paste

Copy this exactly. Do not add quotes or rewrite it:

```text
Reply with one sentence that explains what Claude Code is, written for an absolute beginner.
```

## How to know it worked

Run these three commands. All three should succeed:

```sh
test -s ~/first-prompt.txt && echo "file has content"
grep -q "Claude Code" ~/first-prompt.txt && echo "file mentions Claude Code"
wc -l ~/first-prompt.txt
```

You should see:

```text
file has content
file mentions Claude Code
       6 ~/first-prompt.txt
```

(The line count will vary a bit — anywhere from 4 to ~15 lines is fine. What matters is that the file exists, has content, and references Claude Code.)

A reference version of what the file might look like lives in [`solution/first-prompt.txt`](solution/first-prompt.txt). Your version will differ in the exact wording of the reply (Claude's outputs are not deterministic), and that is the whole point.

## If something went wrong

| Symptom | Fix |
|---|---|
| `claude: command not found` | Module 00 install is incomplete. Re-run `npm i -g @anthropic-ai/claude-code` and reopen your terminal. |
| Claude asks me to log in again | Authorize again in the browser. The token sometimes expires. |
| I typed the prompt at `$`, not `>` | Run `claude` first, then paste at the `>` prompt inside the session. |
| `~/first-prompt.txt` saves to the wrong place | Your editor might be relative to its own folder. Use the literal path `~/first-prompt.txt` or `$HOME/first-prompt.txt`. |
| The reply is much longer than one sentence | That's fine for this exercise. Save whatever you got. Module 03 will teach you how to constrain output. |

## You did it!

If the three checks above all printed their expected lines, you have successfully sent your first prompt to Claude and captured the reply. Move on to [Module 02 — Your first real conversation](../part-02/README.md) when you are ready.
