# Handoff — pricing.py refactor

## What changed
- Replaced 6-level nested conditionals with early `continue` guards and flat logic.
- Extracted tax rates and coupon factors into module-level dicts (`_TAX_RATES`, `_COUPON_FACTORS`).
- Collapsed the shipping ladder from a nested `if/else` to a flat `if/elif/else`.

## Why
The original nesting made it impossible to see the discount and tax logic at a glance.
Every branch ended in `pass`, meaning the structure was hiding no real logic — just noise.
Readability-only refactor; all 8 tests pass byte-identical.

## Risk + rollback
**Risk:** Low. No behavioral change — same rounding, same thresholds, same discount factors.

**Rollback:** The original is preserved in `before/pricing.py`. To revert:
```bash
cp module-08/before/pricing.py <target path>
```

## Watch-outs for the next engineer
- `_COUPON_FACTORS.get(coupon, 1.0)` silently ignores unknown coupons (multiplies by 1). This matches the original `pass` behaviour but is easy to miss if you add a new coupon and forget to register it in the dict.
- VIP discount and coupon are mutually exclusive — VIP takes priority and the coupon is never checked. This was true in the original; the refactor preserves it.
- `unit_price <= 0` skips the item entirely (original behaviour). Negative prices are silently dropped, not an error.
- Tax rate defaults to 10% for any unknown country. If a new country is added, update `_TAX_RATES` — there is no validation or warning for a missing key.
