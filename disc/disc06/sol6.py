def merge(a, b):

    x = next(a)
    y = next(b)

    while True:
        if x < y:
            yield x
            x = next(a)
        if x > y:
            yield y 
            y = next(b)
        if x == y:
            yield x 
            x, y = next(a), next(b)
