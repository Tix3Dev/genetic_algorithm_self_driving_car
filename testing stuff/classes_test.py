import random

class Meow:
    def __init__(self):
        self.name = "Bond" + str(random.randint(1,44))

class Test:
    def __init__(self):
        # self.things = [100, 200, 300]
        self.things = []
        
        for i in range(3):
            self.things.append(Meow())
    
    def foo(self):
        for i, thing in enumerate(self.things):
            print(i, " ->", thing.name)
            # thing.name = "Brotan" + str(random.randint(55,322))
            thing = [12,12,32]

            # okay chaning the whole "thing" doesn't do anything, but changing attributes in it does work, I guess a special property of objects

test = Test()

for thing in test.things:
    print(thing.name)

test.foo()

for thing in test.things:
    print(thing.name)
