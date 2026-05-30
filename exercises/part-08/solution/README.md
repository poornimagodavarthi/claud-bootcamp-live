# Module 8 — Reference Material

The `before/` folder contains a deliberately messy `pricing.py` and a passing test suite. Students copy it to `module-08/after/` and refactor under hard constraints. The `after/` folder here is a **reference refactor** (a real constrained-refactor run) — same tests, same behaviour, readable code.

## Run the tests

```bash
cd before/                 # or: cd after/
pip install pytest         # broken pip? use: uv run --with pytest pytest -q
pytest -q
```

All tests must remain green after the refactor — that's the contract. Both `before/` and `after/` pass the identical suite (8 tests), which is the whole point: a readability refactor must not change behaviour.

## Reference HANDOFF and ARCHITECTURE

A reference `HANDOFF.md` and `ARCHITECTURE.md` live below; instructors compare student output against them but accept any version that satisfies the deliverable checklist in the exercise README.
