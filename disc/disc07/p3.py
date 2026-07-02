class Pet():
    def __init__(self, name, owner):
        self.is_alive = True 
        self.name = name 
        self.owner = owner 
    def eat(self, thing):
        print(self.name + " ate a " + str(thing) + "!")
    def talk(self):
        print(self.name)


class Cat(Pet):
    def __init__(self, name, owner, lives=9):
        super().__init__(name, owner)
        self.lives = lives 

    def talk(self):
        print(self.name + "says meow!")

    def lose_life(self):
        
        if self.is_alive:
            self.lives -= 1
            self.is_alive = (not self.is_alive) if not self.lives else self.is_alive

        else:
            print("Cat cant die anymore than 9 times dude, stop beating it! would ya?")

class NoisyCat(Cat):

    def talk(self):
        for _ in range(2):
            Cat.talk(self)

    def __repr__(self):
        return f"{type(self).__name__}" + "(" + repr(self.name) + ", " + repr(self.owner) + ")"
