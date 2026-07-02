def max_product(s):
    if s == []:
        return 1
    else:
        value = []
        for i in range(len(s)):
            value += [s[i] * max_product(s[i+2:])]
        return max(value)
    


def max_product2(s):

    def helper(remaining):
        if remaining == []:
            return 1
        else:
            return max((remaining[0] * helper(remaining[2:])), 
            helper(remaining[1:]))


    return helper(s)
