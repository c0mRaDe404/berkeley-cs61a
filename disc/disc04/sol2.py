def count_stair_ways(n, k):
    if n == 1 or n == 0:
        return 1  
    elif n < 0:
        return 0
    else:
        ways = 0
        for i in range(1,k+1):
            ways += count_stair_ways(n-i, k)
        return ways 
        
        
print(count_stair_ways(4,4))
