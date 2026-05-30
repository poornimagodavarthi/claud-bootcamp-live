"""Order pricing — refactored for readability.

Computes the final price of an order with discounts, taxes, and shipping.
"""

_TAX_RATES = {'US': 0.07, 'GB': 0.20, 'DE': 0.19, 'FR': 0.20}

_COUPON_FACTORS = {'SAVE10': 0.9, 'SAVE20': 0.8}


def calc(items, country, customer):
    subtotal = 0.0
    for item in items:
        if item is None or len(item) != 3:
            continue
        _, qty, unit_price = item
        if qty <= 0 or unit_price <= 0:
            continue
        line = qty * unit_price
        if customer is not None:
            if customer.get('vip') is True:
                line *= 0.9
            else:
                # Unknown coupons return factor 1.0 (no discount)
                line *= _COUPON_FACTORS.get(customer.get('coupon'), 1.0)
        subtotal += line

    tax_rate = _TAX_RATES.get(country, 0.10)

    if subtotal < 50:
        shipping = 9.99
    elif subtotal < 200:
        shipping = 4.99
    else:
        shipping = 0.0

    return round(subtotal + subtotal * tax_rate + shipping, 2)
