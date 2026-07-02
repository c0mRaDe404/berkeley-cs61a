#print a number N in  reverse order until D is found
def print_num(n):
    def check_num(d):
        temp = n  
        while temp > 0:
            last, temp = temp % 10, temp // 10
            print(last)
            if(last == d):
                break
    return check_num 


