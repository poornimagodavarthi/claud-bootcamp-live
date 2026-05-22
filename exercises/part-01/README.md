# Module 1 — AI Coding Workspace

## Goal

Verify your environment and articulate the AI coding loop in your own words.

## Scenario

You're starting a 4-hour workshop. Before the first prompt, prove your toolchain works and write down — in your own words — how you'll use Claude Code today.

## Starter instructions

1. Open a terminal in a working directory you'll use for the day.
2. Create `module-01/`.
3. Confirm the bootcamp repo is cloned (you ran this in pre-work).

## Claude Code prompt to use

```text
You are onboarding a new engineer who has never used AI-paired coding.
In one short paragraph (max 6 sentences), explain the loop:
Plan → Implement → Test → Review → Commit.
Use the metaphor of directing a junior engineer.
End with one sentence about why skipping the Review step is the most common failure mode.
```

## Manual validation steps

```bash
python3 --version    # 3.11.x or higher
node --version       # v20.x.x or higher
git --version
cat module-01/loop-notes.md   # non-empty, names all 5 steps in order, in your words
```

## Expected deliverable

```text
module-01/
├── environment.txt   # output of the three --version commands
└── loop-notes.md     # your one-paragraph loop explanation
```

## Definition of done

- [ ] `environment.txt` shows valid Python 3.11+, Node 20+, Git versions.
- [ ] `loop-notes.md` names all 5 steps in order.
- [ ] Notes are in *your* words — not Claude's verbatim output.

## Stretch challenge

Write a second paragraph in `loop-notes.md` describing one situation in your day job where the loop would have caught a bug.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `python3` not found | Re-run pre-work install steps (`student-guide.md`). |
| `node` not found | Install Node 20 LTS. |
| WSL2 issues | Always run inside the Ubuntu shell, never PowerShell. |
| Claude Code unresponsive | Verify you're authenticated; pair with a neighbor for module 1 only. |
