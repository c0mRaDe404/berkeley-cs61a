# objective: sum the first N natural numbers
# objective: sum the first N cubes of natural numbers


def cube(n):
    return n * n * n

def summation(n):
    def term(term):
        i, sum = 1, 0
        while i <= n:
            sum, i = sum + term(i), i + 1
        return sum
    return term 

def sum_cubes(n):
    """ Sum the first N cubes for natural numbers

    >>> sum_cubes(5)
    225
    """
    return summation(n)(cube)



print(sum_cubes(5))
