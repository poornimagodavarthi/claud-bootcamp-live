# Architecture — pricing.py

## Data flow

```
caller
  |  items, country, customer
  v
+-------------------------------------------------------+
|  calc()                                               |
|                                                       |
|  +------------------+       +----------------------+  |
|  |  Item loop       | ----> |  _COUPON_FACTORS     |  |
|  |  (guard + line)  |       +----------------------+  |
|  +--------+---------+                                 |
|           | subtotal                                  |
|           v                                           |
|  +------------------+       +----------------------+  |
|  |  Tax lookup      | ----> |  _TAX_RATES          |  |
|  +--------+---------+       +----------------------+  |
|           | tax                                       |
|           v                                           |
|  +------------------+                                 |
|  |  Shipping ladder |                                 |
|  +--------+---------+                                 |
|           | shipping                                  |
|           v                                           |
|    round(subtotal + tax + shipping, 2)                |
+-------------------------------------------------------+
  |  float (final price)
  v
caller
```

## Components

**`_TAX_RATES`** — module-level dict mapping ISO-2 country codes to tax rates.
Falls back to 10% for any unknown country. Input: country string. Output: float rate.

**`_COUPON_FACTORS`** — module-level dict mapping coupon codes to discount multipliers.
Returns `1.0` (no discount) for unknown coupons via `.get(..., 1.0)`.

**Item loop** — iterates `items`, skipping `None` entries, malformed tuples, and
items with non-positive qty or price. Applies VIP (10% off) or coupon discount to
each valid line total, then accumulates into `subtotal`.

**Tax lookup** — single `.get()` against `_TAX_RATES`. Multiplies `subtotal` by the
rate. Input: `subtotal`, `country`. Output: `tax` float.

**Shipping ladder** — three-band `if/elif/else` on `subtotal`: <50 → $9.99,
<200 → $4.99, else free. Input: `subtotal`. Output: `shipping` float.

## Known limitations

1. VIP and coupon discounts are mutually exclusive — VIP always wins; the coupon is silently ignored even if the customer holds both.
2. Unknown coupons produce no error and no discount; a typo in a coupon code fails invisibly.
3. Unknown countries default to 10% tax with no warning — adding a new country without updating `_TAX_RATES` will silently under-tax.
4. Negative or zero unit prices are silently skipped rather than raising an error, hiding bad input from callers.
5. No support for per-item discounts or multiple coupons; the discount model is order-level only.
