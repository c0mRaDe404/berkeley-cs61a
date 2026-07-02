# he wears a jacket if it's below 60 degrees or it is raining
# return True if he will wear a jacket, False otherwise.

def wears_jacket_with_if(temp, raining):
    """
    >>> wears_jacket_with_if(90, False)
    False
    >>> wears_jacket_with_if(40, False)
    True
    >>> wears_jacket_with_if(100, True)
    True
    """
    
    if raining or temp < 60:
        return True
    else:
        return False 

