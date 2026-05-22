# Module 08 — Putting it together (capstone)

> Build a 3-subcommand notes CLI in 30 minutes. Pass the grader. Get your token.

## What you'll build

A working `notes.py` with `add`, `list`, and `delete` subcommands that persist between runs. The grading script `scripts/check-beginner-capstone.sh` will print `PASS <token>` when you're done. The 8-character token goes on your certificate.

## Before you start

- All previous modules (01–07) are done.
- `python3 --version` reports 3.11 or newer.
- 22 minutes.

## Step-by-step

1. Copy the starter to a working location:
   ```sh
   cp -R exercises/beginner/part-08/starter ~/m8
   cd ~/m8
   git init -q && git add . && git commit -q -m "initial"
   ```
2. Open `CLAUDE.md`. It already has the project shape — read it once before starting.
3. Start `claude`.
4. Use a sharp, single prompt (Module 03 pattern). The reference prompt is below.
5. Read the proposed diff (Module 05 habit). Accept only if it matches the contract.
6. Exit Claude. Test by hand:
   ```sh
   python3 notes.py add "buy milk"   # → added: 1
   python3 notes.py list             # → 1<TAB>buy milk
   python3 notes.py delete 1         # → deleted: 1
   python3 notes.py list             # → (empty)
   ```
7. Run the grader:
   ```sh
   cd /Users/$(whoami)/prj/github/Training-Claude-Code-Extended   # or wherever you cloned
   scripts/check-beginner-capstone.sh ~/m8/notes.py
   ```
8. Copy the `PASS <token>` token. You'll paste it into the certificate later (see [`beginner-student-guide.md`](../../../beginner-student-guide.md)).

## The prompt to paste

```text
Act as a careful Python tutor. I have notes.py (currently a stub) and CLAUDE.md (already filled in).

Goal: implement three subcommands so the file matches this contract exactly:
- `python notes.py add "TEXT"` → prints `added: <id>` and exits 0. Persists to notes.json in cwd.
- `python notes.py list` → prints one row per note as `<id><TAB><text>` and exits 0. Empty output if no notes.
- `python notes.py delete <id>` → prints `deleted: <id>` and exits 0. The next add returns the next monotonic id, not the deleted one.
- anything else → prints a usage line on stderr and exits 2.

Constraints: standard library only, ≤ 100 lines, no third-party imports, no comments-only changes.
Format: a single diff against notes.py. Do not modify CLAUDE.md.
```

## How to know it worked

The grader output is the source of truth:

```sh
scripts/check-beginner-capstone.sh ~/m8/notes.py
# → PASS abc12345
```

If you see `PASS <8 hex chars>`, you're done. The token is your proof. Save it.

A reference implementation lives at [`solution/notes.py`](solution/notes.py) — only peek if you're truly stuck.

## If something went wrong

| Symptom | Fix |
|---|---|
| `FAIL: list: expected "1\thello", got "1 hello"` | Use a literal tab, not spaces. `print(f"{n['id']}\t{n['text']}")`. |
| `FAIL: add: expected exit 0, got exit 1` | An exception leaked. Wrap the subcommand dispatch in a clean function that returns an int. |
| `FAIL: list-after-delete: expected "", got "1\thello"` | Your delete is not writing notes.json. Re-save after removing the entry. |
| Next add reuses id 1 after delete | Bug. Compute the next id as `max(existing ids, default=0) + 1`, never `len(notes) + 1`. |
| `scripts/check-beginner-capstone.sh: command not found` | You're running from inside `~/m8`. Run it with the absolute path: `~/prj/github/Training-Claude-Code-Extended/scripts/check-beginner-capstone.sh ~/m8/notes.py`. |

## You did it!

If the grader printed `PASS <token>`, you have built and verified a real Claude-assisted CLI. Render your certificate following [`beginner-student-guide.md`](../../../beginner-student-guide.md). Welcome to the end of Claude Code 101.
