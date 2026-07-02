def add_this_many(x, el, s):
    length = len(s)
    for i in range(length):
        if s[i] == x:
            s.append(el)
