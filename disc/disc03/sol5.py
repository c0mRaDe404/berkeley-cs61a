"""
i start with 2 ... i (n), if n % i == 0, False. else recurse

"""


def is_prime(n):
    
    def p_helper(p):
        if p == 1:
            return True
        if n == 1:
            return False
        if n % p == 0:
            return False
        else:
            return p_helper(p - 1)

    return p_helper(n - 1)

