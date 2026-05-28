# Module 03 — Asking for what you want

> Rewrite a vague prompt into a clear one and save the better answer you get back.

## What you'll build

A file `~/sharp-prompt.txt` with three sections:

1. The vague version of your prompt (one sentence).
2. The clear version using **role + goal + constraint + format**.
3. The reply Claude gave to the clear version.

## Before you start

- Modules 01 and 02 are done.
- You have a short (~30-line) function you're willing to share with Claude. Use the sample in [`starter/sample_function.py`](starter/sample_function.py) if you don't have one handy.
- 12 minutes of focused time.

## Step-by-step

1. Open [`starter/sample_function.py`](starter/sample_function.py) (or your own function) and read it once.
2. Write the **vague** version of your review prompt at the top of `~/sharp-prompt.txt`. Example: `Can you review my code?`.
3. Now rewrite it as a clear prompt with all four pieces:
   - **Role**: e.g. `Act as a careful Python reviewer.`
   - **Goal**: e.g. `Find at most 3 real bugs, in order of severity.`
   - **Constraint**: e.g. `No style nits. No rewrites.`
   - **Format**: e.g. `Numbered list, each entry < 15 words.`
4. Start `claude`, paste your clear prompt followed by the function, press Enter.
5. Copy the reply into `~/sharp-prompt.txt` under section 3.
6. `/exit`.

## The prompt to paste

This is the canonical clear-prompt template. Customise the role and format for your situation:

```text
Act as a careful Python reviewer. I will paste a ~30-line function below. Your goal: find at most 3 real bugs, in order of severity. Constraint: no style nits and no rewrites. Format: a numbered list, each entry under 15 words.

[paste your function here]
```

## How to know it worked

```sh
grep -c '^##' ~/sharp-prompt.txt
grep -i 'role\|goal\|constraint\|format' ~/sharp-prompt.txt | head -5
```

You should see `3` (three H2 headers, one per section) and at least three of the four keywords from the second grep. A working example transcript lives at [`solution/sharp-prompt.example.txt`](solution/sharp-prompt.example.txt).

## If something went wrong

| Symptom | Fix |
|---|---|
| Claude returned style nits even though I forbade them | Your constraint was too soft. Re-prompt: `No style nits. Reject any suggestion that is about naming, spacing, or comments.` |
| The numbered list is missing | The model defaulted to prose. Add `Format: numbered list 1. 2. 3.` more explicitly. |
| The reply rewrote my function | Add `Do not rewrite the function. Only point at the line and explain.` |
| Claude says it cannot review without more context | The function in `starter/` is intentionally small. Tell Claude that and re-send. |

## You did it!

If your `~/sharp-prompt.txt` has the three sections and the third section is a numbered list of at most 3 items, you've used the role + goal + constraint + format pattern. Continue to [Module 04 — Reading code together](../part-04/README.md).
