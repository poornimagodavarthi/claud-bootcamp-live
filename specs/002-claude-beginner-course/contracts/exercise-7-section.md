# Contract — 7-Section Exercise Structure (Beginner)

**Feature**: `002-claude-beginner-course`  
**Applies to**: Every `exercises/beginner/part-NN/README.md`  
**Enforced by**: `scripts/validate.sh` (extension R3.4 + R3.5)  
**Spec**: FR-020, FR-021, FR-022, FR-023, FR-024, FR-025

---

## Required structure

Every beginner exercise README MUST contain, in this exact order, exactly these 7 H2 sections. Below them, the H1 title MUST match the corresponding deck's H1 verbatim.

| # | Section | Heading text (exact) | Constraints |
|---|---------|----------------------|-------------|
| 1 | What you'll build | `## What you'll build` | 1–2 sentences. Name the final artifact (file, screenshot, transcript). |
| 2 | Before you start | `## Before you start` | List prerequisites; first bullet MUST be "You completed Module NN-1" (except Module 01, where it's "You completed Module 00 setup"). |
| 3 | Step-by-step | `## Step-by-step` | Numbered list, ≤ 10 steps, each step exactly one action verb. |
| 4 | The prompt to paste | `## The prompt to paste` | Exactly one fenced code block. Verbatim copy-pasteable (FR-014). |
| 5 | How to know it worked | `## How to know it worked` | A `- [ ]` checkbox list + the exact terminal command to verify + expected stdout. |
| 6 | If something went wrong | `## If something went wrong` | Markdown table with ≥ 3 rows: `\| Symptom \| Cause \| One-line fix \|`. |
| 7 | You did it! | `## You did it!` | One congratulatory line + exactly one optional stretch challenge as a single italic sentence. |

## Directory layout

```text
exercises/beginner/part-NN/
├── README.md         # 7-section contract above
├── starter/          # MUST exist; MUST contain ≥ 1 file. Step 1 is NEVER "create file X."
└── solution/         # MUST exist; MUST contain ≥ 1 non-empty file. Working reference.
```

**Exception**: `exercises/beginner/module-00-setup/` has no `solution/` (its deliverable is the learner's own `first-prompt.txt`); `starter/.keep` is sufficient.

## Time budget

Total time for an exercise (read README + execute the 7 sections) MUST be ≤ 15 minutes for a learner who watched the deck once (FR-020). Reviewers gauge this manually; no automated check.

## Free-plan friendliness (FR-024)

If the exercise's natural demo requires a paid Claude plan, the exercise's "What you'll build" section MUST include a parenthetical "(uses Free-plan equivalent of <feature>)" note and the deck for the same module MUST explain the difference in one line.

## Deliverable concreteness (FR-025)

Section 5's checkbox list MUST resolve to a single named artifact a reviewer can point at:

- a file path the learner produced, OR
- a screenshot the learner saved, OR
- a captured terminal transcript the learner pasted into a file.

"Understanding the concept" is NOT an acceptable deliverable and is rejected at review time.

## Sample skeleton

```markdown
# Module 01 — Meet Claude Code

## What you'll build

A file `first-prompt.txt` containing your terminal's response to `claude --version`. This proves the install is working.

## Before you start

- You completed Module 00 setup.
- You have a terminal open in this folder.

## Step-by-step

1. Open `starter/` in your terminal.
2. Run `claude --version`.
3. Copy the printed line.
4. Paste it into a new file named `first-prompt.txt` in this folder.
5. Save the file.

## The prompt to paste

```text
claude --version
```

## How to know it worked

- [ ] `first-prompt.txt` exists in `exercises/beginner/part-01/`.
- [ ] Its first line starts with `@anthropic-ai/claude-code`.

Verify by running:

```text
$ cat first-prompt.txt
@anthropic-ai/claude-code 2.0.7
```

## If something went wrong

| Symptom | Cause | One-line fix |
|---|---|---|
| `claude: command not found` | The CLI is not on `PATH` | Re-run the install step from Module 00 and reopen your terminal |
| `first-prompt.txt` is empty | You ran the command but didn't paste the output | Re-run `claude --version` and copy the printed line into the file |
| Version line says something other than `@anthropic-ai/claude-code` | Another tool named `claude` is on `PATH` first | Run `which claude` and confirm it points to the npm-installed binary |

## You did it!

You just confirmed Claude Code is alive on your machine.

*Stretch: also run `claude --help` and add its first line to the file.*
```

## Validator failure modes

| Symptom | Validator output |
|---|---|
| Missing or misordered H2 | `<file>:<line>: exercise missing required section '<heading>' at position N` |
| `starter/` missing or empty | `exercises/beginner/part-NN/starter/: required directory missing or empty` |
| `solution/` missing or empty (modules 01–08) | `exercises/beginner/part-NN/solution/: required directory missing or empty` |
| Section 4 has 0 or 2+ fenced code blocks | `<file>:<line>: 'The prompt to paste' MUST contain exactly one fenced code block` |
| Section 6 has < 3 table rows | `<file>:<line>: 'If something went wrong' MUST have at least 3 rows` |
| Title H1 does not match deck H1 | `<file>:1: exercise H1 must match deck H1 (expected '<deck-h1>', got '<exercise-h1>')` |
