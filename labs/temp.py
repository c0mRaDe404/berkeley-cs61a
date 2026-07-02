
operations = {"deposit":0, "withdraw":1, "check_balance":2}

def account(balance):
    def deposit(amount):
        nonlocal balance 
        balance += amount 

    def withdraw(amount):
        nonlocal balance
        assert amount > balance, "Insufficient funds."
            
        balance -= amount

    def check_balance():
        print("Your balance is: ", balance)

    return [deposit, withdraw, check_balance]


def make_account(balance):
    return account(balance)

def do(operation, func_list):
    return func_list[operations[operation.lower()]]
