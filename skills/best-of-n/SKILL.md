---
name: best-of-n
description: Run a Best-of-N solution-comparison workflow, score each candidate on a tradeoff matrix, and select the winner.
---

## Purpose

Generates N independent solutions to a stated problem, scores each
against a weighted tradeoff matrix (correctness, readability, performance,
safety), and selects the winner with a written rationale.

## When to use it

- When multiple valid approaches exist and you need a principled way to choose one.
- Before committing to an implementation strategy for a non-trivial feature.
- When reviewing competing pull requests or design proposals.
- After generating an AI solution that feels uncertain — generate alternatives and compare.

## Prompt body

```text
Run a Best-of-N comparison for the following problem:

PROBLEM: PROBLEM_STATEMENT
N: NUMBER_OF_CANDIDATES (default: 3)

Steps:
1. Generate NUMBER_OF_CANDIDATES independent solutions. Label them Candidate A, B, C, …
   Each candidate must be a complete, runnable implementation — no stubs.

2. Score each candidate on the following criteria (1–5 scale):
   - Correctness: handles all stated requirements and edge cases
   - Readability: clear names, flat structure, no unnecessary abstraction
   - Performance: avoids unnecessary work, scales reasonably
   - Safety: no injection risks, validates inputs at boundaries

3. Produce a scoring table:
   | Criterion    | A | B | C |
   |-------------|---|---|---|
   | Correctness  |   |   |   |
   | Readability  |   |   |   |
   | Performance  |   |   |   |
   | Safety       |   |   |   |
   | **Total**    |   |   |   |

4. Declare the winner. Write 2–3 sentences explaining why it scored highest
   and note any strengths worth grafting from the runners-up.
```

## Expected inputs

- `PROBLEM_STATEMENT` — a clear description of the function, endpoint, or module to implement.
- `NUMBER_OF_CANDIDATES` — how many solutions to generate (default: 3).
- Optional: additional scoring criteria or weights specific to the project.

## Expected outputs

- N complete candidate implementations, labelled A, B, C, …
- A filled scoring table (4 criteria × N candidates).
- A winner declaration with written rationale.

## Worked example

**Scenario:** Choose the best implementation of a function that flattens a nested list.

**Invocation:**
```
/best-of-n PROBLEM_STATEMENT="Write a function flatten(lst) that flattens an arbitrarily nested list of integers." NUMBER_OF_CANDIDATES=3
```

**Expected output (excerpt):**
```
Candidate A — recursive
def flatten(lst):
    for item in lst:
        if isinstance(item, list): yield from flatten(item)
        else: yield item

Candidate B — iterative stack
...

| Criterion    | A | B | C |
|-------------|---|---|---|
| Correctness  | 5 | 5 | 4 |
| Readability  | 5 | 3 | 4 |
| Performance  | 3 | 5 | 4 |
| Safety       | 4 | 4 | 4 |
| Total        |17 |17 |16 |

Winner: Candidate A — tied on total but preferred for readability.
Consider grafting Candidate B's iterative approach if stack depth is a concern.
```
