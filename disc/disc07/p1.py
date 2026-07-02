class MinList:

    def __init__(self):
        self.items = []
        self.size = 0 

    def append(self, item):
        self.items.append(item)
        self.size += 1 

    def pop(self):

        if self.size <= 0:
            print("List is empty!")
            return 
        e = min(self.items) 
        self.items.remove(e)
        self.size -= 1
        return e 
    def __repr__(self):
        return f"{self.items}"
