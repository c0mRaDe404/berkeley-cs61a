def count_stair_ways(n):
    if n == 1 or n == 0:
        return 1

    elif n < 0:
        return 0

    else:
        return count_stair_ways(n-1) + count_stair_ways(n-2)
