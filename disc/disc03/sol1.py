def mul(x, y):
    """
    >>> mul(5, 3)
    15

    """

    if y == 1:
        return x
    else:
        return x + mul(x, y - 1)

