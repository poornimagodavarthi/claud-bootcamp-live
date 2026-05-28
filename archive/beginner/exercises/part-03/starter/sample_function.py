def average_positive(numbers):
    """Return the average of the positive numbers in the list.

    If there are no positive numbers, return 0.
    """
    total = 0
    count = 0
    for n in numbers:
        if n > 0:
            total += n
            count += 1
    # Bug #1: integer division can lose precision.
    # Bug #2: when count is 0 we divide by zero (caught by the if, but the
    #         comment says 'return 0' — we actually return 0.0 only sometimes).
    # Bug #3: numbers can be None, raising TypeError on `n > 0` comparison
    #         instead of a friendly error.
    if count == 0:
        return 0
    return total // count
