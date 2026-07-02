def group_by(s, fn):
    grouped = {}
    for e in s:
        key = fn(e)
        if key in grouped:
            grouped.get(key).append(e)
        else:
            grouped[key] = [e] 
    return grouped
