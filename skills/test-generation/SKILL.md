---
name: test-generation
description: Generate a meaningful test suite for a target file or function, covering happy paths, edge cases, and error paths.
---

## Purpose

Reads a target source file or function and produces a test file that
covers the happy path, boundary conditions, and error paths — using the
project's existing test framework and conventions.

## When to use it

- When a new module or function has no tests yet.
- After a refactor, to verify behavior is preserved with regression tests.
- When test coverage is below an acceptable threshold for a critical path.
- Before adding a feature, to write tests first in a TDD workflow.

## Prompt body

```text
Generate a test suite for TARGET using the project's test framework.

Steps:
1. Read TARGET and identify every public function or endpoint.
2. For each, write tests covering:
   a. Happy path — valid inputs, expected output.
   b. Boundary conditions — empty input, zero, maximum value, single element.
   c. Error path — invalid input, missing required fields, out-of-range values.
3. Use the test framework already present in the project (pytest, unittest, etc.).
4. Follow the naming and import conventions of any existing test files.
5. Do not mock internal logic unless testing at a boundary (HTTP, DB, filesystem).
6. Write one assert per test where possible.

Output: a single test file ready to run with no modification.
Do not include placeholder tests — every test must make a real assertion.
```

## Expected inputs

- `TARGET` — path to the source file or function to test (e.g. `./pricing.py`).
- Optionally: the test framework to use if none is detected (e.g. `pytest`).

## Expected outputs

- A single test file (e.g. `test_pricing.py`) written alongside the source file.
- Tests grouped by function, with descriptive names (`test_<fn>_<scenario>`).

## Worked example

**Scenario:** Generate tests for a `calc()` function in `pricing.py`.

**Invocation:**
```
/test-generation TARGET=pricing.py
```

**Expected output (excerpt):**
```python
from pricing import calc

def test_calc_simple_purchase():
    assert calc([("widget", 2, 10.0)], "US", None) == 31.39

def test_calc_vip_discount():
    assert calc([("widget", 1, 100.0)], "US", {"vip": True}) == 105.29

def test_calc_skips_none_item():
    assert calc([None, ("widget", 1, 10.0)], "US", None) == 20.69

def test_calc_free_shipping_over_200():
    items = [("widget", 5, 50.0)]
    assert calc(items, "FR", None) == 300.0
```
