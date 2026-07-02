def make_func_repeater(f, x):
    """
    >>> incr_1 = make_func_repeater(lambda x: x + 1, 1)
    >>> incr_1(2) #same as f(f(x))
    3
    >>> incr_1(5)
    6
    """
    def repeat(y):

        if y == 0:
            return x 
        
        return make_func_repeater(f, f(x))(y - 1)
        

    return repeat
