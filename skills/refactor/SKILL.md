---
name: refactor
description: Refactor a target file under stated constraints, preserve all existing behavior, and emit a unified diff plan.
---

## Purpose

Applies a set of caller-specified refactor constraints to a source file
— readability, early returns, naming, structure — without changing public
signatures or observable behavior, and outputs a unified diff.

## When to use it

- When code review feedback asks for readability improvements without a behavior change.
- After generating AI code that is correct but deeply nested or hard to follow.
- Before handing off a module to another engineer who needs to maintain it.
- When a linter or style guide flags structural issues that need systematic fixing.

## Prompt body

```text
Refactor TARGET under the following hard constraints:

CONSTRAINTS (caller supplies these — default set below if none provided):
- No new files. No new dependencies.
- Public function signatures unchanged. Module-level imports unchanged.
- Behavior on all existing tests must be byte-identical.
- Replace nested conditionals with early returns where it shortens code.
- Rename local variables only when the new name is materially clearer.
- No comments unless they explain a non-obvious *why*.

Steps:
1. Read TARGET in full.
2. Identify every violation of the constraints.
3. Apply the minimal change that fixes each violation.
4. Verify (by inspection) that no public signature changed.
5. Output a unified diff (--- before, +++ after). No prose outside the diff.
```

## Expected inputs

- `TARGET` — path to the file to refactor (e.g. `./pricing.py`).
- `CONSTRAINTS` — optional list of additional or replacement constraints (plain text bullets).

## Expected outputs

- A unified diff (`--- a/TARGET` / `+++ b/TARGET`) ready to apply with `git apply`.
- No prose, no explanation outside the diff itself.

## Worked example

**Scenario:** Refactor a pricing module with 6-level nesting.

**Invocation:**
```
/refactor TARGET=pricing.py
```

**Expected output (excerpt):**
```diff
--- a/pricing.py
+++ b/pricing.py
@@ -6,6 +6,9 @@
+_TAX_RATES = {'US': 0.07, 'GB': 0.20, 'DE': 0.19, 'FR': 0.20}
+_COUPON_FACTORS = {'SAVE10': 0.9, 'SAVE20': 0.8}
+
 def calc(items, country, customer):
-    t = 0
-    for it in items:
-        if it != None:
+    subtotal = 0.0
+    for item in items:
+        if item is None or len(item) != 3:
+            continue
```
