def keep_ints(cond, n):
    """Print out all integers 1 to n where cond(n) is true

    >>> def is_even(x):
    ...     return x % 2 == 0
    >>> keep_ints(is_even, 5)
    2
    4
    
    """

    i = 1
    while i <= n:
        if cond(i):
            print(i)
        i += 1



