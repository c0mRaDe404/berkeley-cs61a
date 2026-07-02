def split(x):
    return x % 10, x // 10


def merge(n1, n2):
    """ Merges two numbers
    >>> merge(31, 42)
    4321
    >>> merge(21, 0)
    21
    >>> merge (21, 31)
    3211
    """

    if n1 == 0:
        return n2
    if n2 == 0:
        return n1
    else:
        r1, d1 = split(n1)
        r2, d2 = split(n2)

        if r1 > r2:
            return merge(d2, n1)  * 10 + r2
        elif r2 > r1:
            return merge(d1, n2)  * 10 + r1
    return merge(d1,n2) * 10 + r1

