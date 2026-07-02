# input number N
# smallest factor K 

# keep dividing N by K if the result is zero 

def prime_factorization(n):
    
    k = 2
    while n > 1:
        while n % k == 0:
            print(k)
            n = n // k 
        else:
            k = k + 1

