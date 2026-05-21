# Code Review Rubric — for AI-generated code

> **What this is**: a sample student-authored rubric. **Replace it with your own** during the Module 5 lab. Your rubric should reflect *your* blind spots, not this one's.
>
> **What this is not**: the instructor's grading rubric for the workshop. That lives at [`assessments/rubric.md`](../../assessments/rubric.md) and grades the assessment, not your code.

## Sample rubric (replace before submitting)

For each AI-generated diff, answer yes/no in ≤ 30 seconds per item:

- [ ] **Boundaries**: are empty inputs, zero, negative, very large, and the maximum index all handled and tested?
- [ ] **Error paths**: does every `try` have a meaningful `except`/`catch` (not bare `pass`/swallow)?
- [ ] **Type assumptions**: any place where `None`/`null`/`undefined` could sneak through? Is it explicit?
- [ ] **Hidden state**: did Claude introduce a global, a module-level cache, or a shared connection that survives across requests?
- [ ] **Concurrency**: is there any code path that would race if two requests hit it at once?
- [ ] **External calls**: does the code make a network or filesystem call I didn't ask for?
- [ ] **Test parity**: does the test suite exercise the *same* code paths the production caller will?

## Pass / fail

You pass the review if and only if **all 7 items are checked**. One unchecked = back to Claude with a targeted fix prompt.

---

## Authoring tips for your own rubric

1. Start from this template, then **delete** any item that doesn't reflect a bug *you* have shipped (or watched a colleague ship).
2. **Add** at least one item drawn from your own track (Python or Node) and your own framework (FastAPI vs Hono).
3. Each item must be a **yes/no question** answerable in ≤ 30 seconds.
4. Cap at 8 items. Longer rubrics get skipped.
