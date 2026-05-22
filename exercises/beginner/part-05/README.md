# Module 05 — Editing one file safely

> Let Claude edit a file, then undo the edit with `git restore`. Both halves matter.

## What you'll build

A `hello.py` that ends the exercise **identical** to how it started, because you proved you can undo any Claude edit with one command.

## Before you start

- Modules 01–04 are done.
- `git --version` works (check Module 00 if not).
- 15 minutes.

## Step-by-step

1. Copy the starter folder to a working location and initialise Git:
   ```sh
   cp -R exercises/beginner/part-05/starter ~/m5
   cd ~/m5
   git init -q
   git add . && git commit -q -m "initial"
   git status      # should say: nothing to commit, working tree clean
   ```
2. Start `claude`.
3. Paste this prompt:
   ```text
   Open hello.py. Add a one-line docstring to the greet() function explaining what it returns. Do not change behaviour or formatting.
   ```
4. **Read the diff** before pressing `y`. Confirm it only adds one `"""..."""` line.
5. Accept the change. `/exit`.
6. Confirm the file changed: `git diff hello.py` should show one added line.
7. Now **undo** the change to prove the safety net works:
   ```sh
   git restore hello.py
   git diff hello.py     # should be empty
   ```

## The prompt to paste

```text
Open hello.py. Add a one-line docstring to the greet() function explaining what it returns. Do not change behaviour or formatting.
```

## How to know it worked

After step 7, all three of these must be true:

```sh
git status                    # → nothing to commit, working tree clean
diff hello.py exercises/beginner/part-05/starter/hello.py   # → no output
git log --oneline             # → exactly 1 commit ("initial")
```

If the diff is empty and the working tree is clean, you've completed a full propose → accept → undo cycle. The reference "after-accept" state is at [`solution/hello.py`](solution/hello.py).

## If something went wrong

| Symptom | Fix |
|---|---|
| `git restore hello.py` says `error: pathspec` | You're not in `~/m5`. `cd ~/m5` and try again. |
| Claude proposed extra changes (renamed function, added imports) | Reject. Re-prompt with `Only add a docstring. Do not change anything else.` |
| I accepted the diff and now want it back after restoring | Re-run the prompt; Claude will propose the same one-line docstring again. |
| `git diff` shows nothing even after I accepted | You probably exited without saving. Re-run the prompt. |

## You did it!

If you can both apply and undo a Claude edit on demand, you have the entire beginner safety story. Continue to [Module 06 — CLAUDE.md cheat sheet](../part-06/README.md).
