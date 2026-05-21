# Module 07 — Safer & smarter

> Redact a fake config file with three planted leaks. Then ask Claude about the safe version only.

## What you'll build

A redacted copy `leaky_config.redacted.txt` in your home directory, plus a transcript proving you only ever showed Claude the safe version.

> **Note**: every leak in the starter file is a deliberately obvious placeholder (`hunter2`, `alice@example.com`, etc.). Do **not** use real secrets or real names in this exercise.

## Before you start

- Modules 01–06 are done.
- 10 minutes.

## Step-by-step

1. Open [`starter/leaky_config.txt`](starter/leaky_config.txt). Find the three planted leaks (one secret, one PII, one proprietary string).
2. Make a copy and redact each leak in your editor:
   ```sh
   cp exercises/beginner/part-07/starter/leaky_config.txt ~/leaky_config.redacted.txt
   # then edit ~/leaky_config.redacted.txt
   ```
   - Replace secrets with the literal word `REDACTED`.
   - Replace personal names/emails with `Alice / alice@example.com`.
   - Replace proprietary strings with `INTERNAL`.
3. Confirm the redacted file no longer contains any of the original leak markers:
   ```sh
   ! grep -E 'hunter2|alice\.smith|ProjectChimera' ~/leaky_config.redacted.txt && echo "clean"
   ```
4. Start `claude`. Paste the prompt below with the **redacted** file only.
5. `/exit`.

## The prompt to paste

```text
This config fails to connect. Without inventing values, tell me what is structurally wrong with it — empty fields, wrong types, missing keys. Do not ask for the real values.

[paste the redacted file here]
```

## How to know it worked

```sh
test -s ~/leaky_config.redacted.txt && echo "file exists"
! grep -E 'hunter2|alice\.smith|ProjectChimera' ~/leaky_config.redacted.txt && echo "clean"
grep -c REDACTED ~/leaky_config.redacted.txt    # → at least 1
```

A correctly-redacted reference is at [`solution/leaky_config.redacted.txt`](solution/leaky_config.redacted.txt).

## If something went wrong

| Symptom | Fix |
|---|---|
| `grep` still finds `hunter2` | You missed the secret. Open the file and search again. |
| I redacted everything and now the file is meaningless | Over-redaction. Keep the **structure** (keys, types, shape); replace only the values. |
| I sent the original by accident | This is exactly the scenario the module is about. In a real situation: rotate the secret, tell your security team, learn the lesson. |

## You did it!

If the redacted file is clean and Claude was only ever shown that version, you've practised the most important security habit of the workshop. Continue to [Module 08 — Putting it together](../part-08/README.md) for the capstone.
