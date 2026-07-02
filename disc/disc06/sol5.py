def filter(iterable, fn):
    for e in iterable:
        if fn(e):
            yield e
